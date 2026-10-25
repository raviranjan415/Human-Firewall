"""User, role, preference, organization and assignment models."""

from __future__ import annotations

from datetime import datetime, timezone
import logging

import argon2
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

logger = logging.getLogger(__name__)

# Argon2id password hasher instance
_ph = argon2.PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MiB
    parallelism=2,
    hash_len=32,
    type=argon2.Type.ID,
)

# Role constants used across the application
ROLE_LEARNER = "learner"
ROLE_INSTRUCTOR = "instructor"
ROLE_ADMIN = "admin"
ROLE_ORG_ADMIN = "org_admin"
ROLES = (ROLE_LEARNER, ROLE_INSTRUCTOR, ROLE_ADMIN, ROLE_ORG_ADMIN)


def utcnow() -> datetime:
    """Timezone-aware UTC timestamp (stored naive in SQLite)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))

    users = db.relationship("User", back_populates="role")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Role {self.name}>"


# Import Organization from app.models.organization so there is a single canonical model.
from app.models.organization import (  # noqa: E402
    Organization,
    OrganizationMembership,
    STATUS_ACTIVE,
    ORG_ROLE_ADMIN,
    ORG_ROLE_TP_COORDINATOR,
)


class User(db.Model, UserMixin, TimestampMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120))
    avatar_url = db.Column(db.String(500))
    locale = db.Column(db.String(8), default="en", nullable=False)
    timezone = db.Column(db.String(64), default="Asia/Kolkata", nullable=False)
    # Explorer / Challenge / Professional learning experience.
    learning_mode = db.Column(db.String(24), default="explorer", nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)

    # Aggregated gamification counters
    xp_total = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False)
    current_streak = db.Column(db.Integer, default=0, nullable=False)
    longest_streak = db.Column(db.Integer, default=0, nullable=False)
    last_activity_date = db.Column(db.Date)

    # Login protection
    failed_login_count = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)

    role = db.relationship("Role", back_populates="users")
    organization = db.relationship("Organization", foreign_keys=[organization_id])
    memberships = db.relationship(
        "OrganizationMembership",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="OrganizationMembership.joined_at.desc()",
    )
    preference = db.relationship(
        "UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    progress_records = db.relationship(
        "UserProgress", back_populates="user", cascade="all, delete-orphan"
    )
    xp_transactions = db.relationship(
        "XPTransaction", back_populates="user", cascade="all, delete-orphan"
    )

    # --- password handling (Argon2id with legacy PBKDF2 transparent upgrade) ---
    def set_password(self, raw_password: str) -> None:
        """Store a salted Argon2id hash — state-of-the-art password security."""
        self.password_hash = _ph.hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verify password against Argon2id hash or legacy PBKDF2 hash with transparent upgrade."""
        if not self.password_hash:
            return False
        if self.password_hash.startswith("$argon2"):
            try:
                _ph.verify(self.password_hash, raw_password)
                if _ph.check_needs_rehash(self.password_hash):
                    self.set_password(raw_password)
                return True
            except (argon2.exceptions.VerifyMismatchError, argon2.exceptions.VerificationError, argon2.exceptions.InvalidHashError):
                return False
        else:
            # Fallback to werkzeug check_password_hash for existing PBKDF2 / scrypt hashes
            if check_password_hash(self.password_hash, raw_password):
                # Upgrade legacy hash seamlessly to Argon2id upon successful sign in
                try:
                    self.set_password(raw_password)
                    db.session.commit()
                except Exception:
                    pass
                return True
            return False

    # --- convenience helpers ---------------------------------------------
    @property
    def name(self) -> str:
        return self.display_name or self.username

    @property
    def role_name(self) -> str:
        return self.role.name if self.role else ROLE_LEARNER

    @property
    def is_admin(self) -> bool:
        return self.role_name == ROLE_ADMIN

    @property
    def is_instructor(self) -> bool:
        return self.role_name == ROLE_INSTRUCTOR

    @property
    def is_org_admin(self) -> bool:
        if self.role_name in (ROLE_ADMIN, ROLE_ORG_ADMIN):
            return True
        for m in self.memberships:
            if m.status == STATUS_ACTIVE and m.role in (ORG_ROLE_ADMIN, ORG_ROLE_TP_COORDINATOR):
                return True
        return False

    @property
    def is_learner(self) -> bool:
        return self.role_name == ROLE_LEARNER

    def has_role(self, *names: str) -> bool:
        return self.role_name in names

    @property
    def joined_organizations(self) -> list[Organization]:
        """All organizations where this user has an active membership."""
        orgs = []
        for m in self.memberships:
            if m.status == STATUS_ACTIVE and m.organization and m.organization.is_active:
                orgs.append(m.organization)
        return orgs

    @property
    def active_organization(self) -> Organization | None:
        """The active workspace organization for this session."""
        if self.organization_id:
            org = db.session.get(Organization, self.organization_id)
            if org and org.is_active:
                return org
        active_list = self.joined_organizations
        return active_list[0] if active_list else None

    def get_membership(self, org_id: int) -> OrganizationMembership | None:
        """Retrieve membership record for a given organization ID."""
        for m in self.memberships:
            if m.organization_id == org_id:
                return m
        return None

    def is_org_admin_for(self, org_id: int) -> bool:
        """Verify if user has administrative rights for a specific organization."""
        if self.is_admin:
            return True
        membership = self.get_membership(org_id)
        return bool(membership and membership.status == STATUS_ACTIVE and membership.role in (ORG_ROLE_ADMIN, ORG_ROLE_TP_COORDINATOR))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User {self.username} ({self.role_name})>"


class UserPreference(db.Model, TimestampMixin):
    """Accessibility and personalisation preferences."""

    __tablename__ = "user_preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    language = db.Column(db.String(8), default="en", nullable=False)
    text_size = db.Column(db.String(16), default="normal", nullable=False)
    reduce_motion = db.Column(db.Boolean, default=False, nullable=False)
    high_contrast = db.Column(db.Boolean, default=False, nullable=False)
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)
    public_leaderboard = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship("User", back_populates="preference")


class GroupMembership(db.Model, TimestampMixin):
    __tablename__ = "group_memberships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    group_name = db.Column(db.String(120))
    role_in_group = db.Column(db.String(32), default="member", nullable=False)

    organization = db.relationship("Organization", back_populates="members")

    __table_args__ = (
        db.UniqueConstraint("user_id", "organization_id", "group_name", name="uq_group_member"),
    )


class LearningAssignment(db.Model, TimestampMixin):
    """An instructor or HR administrator assigns training to a learner or cohort."""

    __tablename__ = "learning_assignments"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    path_id = db.Column(db.Integer, db.ForeignKey("learning_paths.id"))
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id", ondelete="CASCADE"))
    course_type = db.Column(db.String(32), default="path", nullable=False)  # path | lab | game
    cohort = db.Column(db.String(120))
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    assigner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(24), default="assigned", nullable=False)  # assigned | in_progress | completed | overdue
    notes = db.Column(db.Text)
    completed_at = db.Column(db.DateTime)

    assignee = db.relationship("User", foreign_keys=[assignee_id])
    assigner = db.relationship("User", foreign_keys=[assigner_id])
    organization = db.relationship("Organization")
    learning_path = db.relationship("LearningPath")
    lab = db.relationship("Lab")

