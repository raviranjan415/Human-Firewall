"""Organization, multi-tenant workspace, eligible-member registry and subscription models."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import secrets

from app.extensions import db
from app.models.user import TimestampMixin, utcnow

# Organization subscription plans
PLAN_STARTER = "starter"
PLAN_PROFESSIONAL = "professional"
PLAN_ENTERPRISE = "enterprise"
ORGANIZATION_PLANS = {
    PLAN_STARTER: {
        "name": "Starter Academy",
        "seats": 50,
        "price_per_seat_annual": 12,
        "features": ["All 100 Practical Labs", "Video Lessons & Comics", "Basic Reporting", "Certificate Verification"],
    },
    PLAN_PROFESSIONAL: {
        "name": "Professional Campus / Enterprise",
        "seats": 250,
        "price_per_seat_annual": 9,
        "features": ["All Starter Features", "Custom Cohorts & Deadlines", "CSV Registry Bulk Import", "HR-Assisted Account Recovery", "Exportable PDF/CSV Reports", "Priority Support"],
    },
    PLAN_ENTERPRISE: {
        "name": "Global Enterprise / Multi-Campus",
        "seats": 1000,
        "price_per_seat_annual": 6,
        "features": ["All Professional Features", "Unlimited Workspaces & Cohorts", "Custom Security Training Scenarios", "Dedicated Account Manager", "SSO & Advanced Tenant Isolation", "99.99% SLA"],
    },
}

# Member enrollment statuses (Section 7.5 of requirements)
STATUS_ELIGIBLE = "eligible"                          # Eligible — Not Registered
STATUS_INVITATION_SENT = "invitation_sent"            # Invitation Sent
STATUS_REGISTRATION_STARTED = "registration_started"  # Registration Started
STATUS_AWAITING_VERIFICATION = "awaiting_verification" # Awaiting Email Verification
STATUS_PENDING_APPROVAL = "pending_approval"          # Pending Approval
STATUS_ACTIVE = "active"                              # Active Member
STATUS_SUSPENDED = "suspended"                        # Suspended
STATUS_REVOKED = "revoked"                            # Revoked

ENROLLMENT_STATUSES = (
    STATUS_ELIGIBLE,
    STATUS_INVITATION_SENT,
    STATUS_REGISTRATION_STARTED,
    STATUS_AWAITING_VERIFICATION,
    STATUS_PENDING_APPROVAL,
    STATUS_ACTIVE,
    STATUS_SUSPENDED,
    STATUS_REVOKED,
)

# Membership roles within an organization
ORG_ROLE_MEMBER = "member"
ORG_ROLE_ADMIN = "org_admin"
ORG_ROLE_TP_COORDINATOR = "tp_coordinator"
ORG_ROLES = (ORG_ROLE_MEMBER, ORG_ROLE_ADMIN, ORG_ROLE_TP_COORDINATOR)


def generate_org_code(prefix: str = "HF-ORG") -> str:
    """Generate a unique, cryptographically secure organization code (e.g. HF-ORG-7K29Q)."""
    charset = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"  # remove ambiguous 0/O, 1/I
    suffix = "".join(secrets.choice(charset) for _ in range(5))
    return f"{prefix}-{suffix}"


def hash_token(raw_token: str) -> str:
    """Cryptographic SHA-256 hash for tokens and passcodes."""
    return hashlib.sha256(raw_token.strip().encode("utf-8")).hexdigest()


class Organization(db.Model, TimestampMixin):
    """Organization tenant workspace."""

    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), unique=True, nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    org_code = db.Column(db.String(32), unique=True, nullable=False, index=True, default=generate_org_code)
    domain = db.Column(db.String(120))  # e.g. "stanford.edu" or "acme.corp"
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Enrollment controls
    require_passcode = db.Column(db.Boolean, default=False, nullable=False)
    passcode_hash = db.Column(db.String(255))
    require_approval = db.Column(db.Boolean, default=False, nullable=False)

    # Seat & Subscription entitlement
    seats_purchased = db.Column(db.Integer, default=50, nullable=False)
    subscription_plan = db.Column(db.String(32), default=PLAN_STARTER, nullable=False)
    subscription_status = db.Column(db.String(32), default="active", nullable=False)  # active, trial, past_due, expired, cancelled
    subscription_expires_at = db.Column(db.DateTime)
    contact_email = db.Column(db.String(255))
    contact_name = db.Column(db.String(160))

    # Relationships
    members = db.relationship("GroupMembership", back_populates="organization", cascade="all, delete-orphan")
    memberships = db.relationship(
        "OrganizationMembership",
        back_populates="organization",
        cascade="all, delete-orphan",
        order_by="OrganizationMembership.joined_at.desc()",
    )
    eligible_members = db.relationship(
        "EligibleMember", back_populates="organization", cascade="all, delete-orphan"
    )
    invitations = db.relationship(
        "OrgInvitation", back_populates="organization", cascade="all, delete-orphan"
    )
    subscriptions = db.relationship(
        "OrganizationSubscription", back_populates="organization", cascade="all, delete-orphan"
    )
    invoices = db.relationship(
        "SubscriptionInvoice", back_populates="organization", cascade="all, delete-orphan"
    )

    def set_passcode(self, raw_passcode: str) -> None:
        """Hash and store an enrollment passcode."""
        if not raw_passcode:
            self.passcode_hash = None
            self.require_passcode = False
        else:
            self.passcode_hash = hash_token(raw_passcode)
            self.require_passcode = True

    def check_passcode(self, raw_passcode: str) -> bool:
        """Verify enrollment passcode."""
        if not self.require_passcode or not self.passcode_hash:
            return True
        return self.passcode_hash == hash_token(raw_passcode or "")

    def rotate_org_code(self) -> str:
        """Generate a new unique organization code while preserving existing memberships."""
        new_code = generate_org_code()
        while Organization.query.filter_by(org_code=new_code).first() is not None:
            new_code = generate_org_code()
        self.org_code = new_code
        return new_code

    @property
    def occupied_seats(self) -> int:
        """Active members occupying a paid seat."""
        return OrganizationMembership.query.filter_by(
            organization_id=self.id, status=STATUS_ACTIVE
        ).count()

    @property
    def pending_seats(self) -> int:
        """Pending approval or invited members awaiting enrollment."""
        return OrganizationMembership.query.filter_by(
            organization_id=self.id, status=STATUS_PENDING_APPROVAL
        ).count()

    @property
    def available_seats(self) -> int:
        """Remaining seats available for enrollment."""
        return max(0, self.seats_purchased - self.occupied_seats)

    def can_enroll(self) -> tuple[bool, str]:
        """Server-side seat entitlement & subscription validation."""
        if not self.is_active:
            return False, "This organization workspace is currently disabled."
        if self.subscription_status not in ("active", "trial"):
            return False, "This organization subscription is inactive or expired."
        if self.subscription_expires_at and self.subscription_expires_at < utcnow():
            return False, "This organization subscription has expired."
        if self.available_seats <= 0:
            return False, "All purchased training seats are currently occupied. Contact your organization administrator."
        return True, ""

    def __repr__(self) -> str:
        return f"<Organization {self.name} ({self.org_code})>"


class OrganizationMembership(db.Model, TimestampMixin):
    """Authorized membership linking an individual user to an organization workspace."""

    __tablename__ = "organization_memberships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role = db.Column(db.String(32), default=ORG_ROLE_MEMBER, nullable=False)  # member | org_admin | tp_coordinator
    department = db.Column(db.String(120))
    cohort = db.Column(db.String(120))
    registration_id = db.Column(db.String(120), index=True)  # Org-scoped ID (University Reg / Emp ID)
    status = db.Column(db.String(32), default=STATUS_ACTIVE, nullable=False)  # active | pending_approval | suspended | revoked
    joined_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship("User", back_populates="memberships")
    organization = db.relationship("Organization", back_populates="memberships")

    __table_args__ = (
        db.UniqueConstraint("user_id", "organization_id", name="uq_user_organization_membership"),
        db.Index("ix_org_reg_id", "organization_id", "registration_id"),
    )

    @property
    def is_admin(self) -> bool:
        return self.role in (ORG_ROLE_ADMIN, ORG_ROLE_TP_COORDINATOR)

    def __repr__(self) -> str:
        return f"<OrgMembership User:{self.user_id} Org:{self.organization_id} Role:{self.role}>"


class EligibleMember(db.Model, TimestampMixin):
    """Pre-approved registry of eligible students or employees uploaded by HR / T&P."""

    __tablename__ = "eligible_members"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    identifier = db.Column(db.String(120), nullable=False, index=True)  # Student Reg / Emp ID
    full_name = db.Column(db.String(160))
    approved_email = db.Column(db.String(255), index=True)
    department = db.Column(db.String(120))
    cohort = db.Column(db.String(120))
    training_group = db.Column(db.String(120))
    status = db.Column(db.String(32), default=STATUS_ELIGIBLE, nullable=False)  # eligible | invitation_sent | registered | ...
    claimed_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    claimed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    organization = db.relationship("Organization", back_populates="eligible_members")
    claimed_by = db.relationship("User", foreign_keys=[claimed_by_user_id])

    __table_args__ = (
        # Scoped strictly to the issuing organization: two different orgs can have the same identifier!
        db.UniqueConstraint("organization_id", "identifier", name="uq_org_eligible_identifier"),
        db.Index("ix_org_identifier_status", "organization_id", "identifier", "status"),
    )

    def __repr__(self) -> str:
        return f"<EligibleMember Org:{self.organization_id} ID:{self.identifier} Status:{self.status}>"


class OrgInvitation(db.Model, TimestampMixin):
    """Time-limited, single-use invitation for organization onboarding."""

    __tablename__ = "org_invitations"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash = db.Column(db.String(128), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255))
    identifier = db.Column(db.String(120))  # Optional pre-linked Reg ID / Emp ID
    role = db.Column(db.String(32), default=ORG_ROLE_MEMBER, nullable=False)
    department = db.Column(db.String(120))
    cohort = db.Column(db.String(120))
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    revoked = db.Column(db.Boolean, default=False, nullable=False)

    organization = db.relationship("Organization", back_populates="invitations")
    created_by = db.relationship("User", foreign_keys=[created_by_id])

    @property
    def is_valid(self) -> bool:
        return not self.revoked and self.used_at is None and self.expires_at > utcnow()


class EmailVerificationToken(db.Model):
    """Cryptographic, single-use email verification token."""

    __tablename__ = "email_verification_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash = db.Column(db.String(128), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship("User")

    @property
    def is_valid(self) -> bool:
        return self.used_at is None and self.expires_at > utcnow()


class PasswordResetToken(db.Model):
    """Cryptographic, single-use password reset token with anti-replay invalidation."""

    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash = db.Column(db.String(128), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    user = db.relationship("User")

    @property
    def is_valid(self) -> bool:
        return self.used_at is None and self.expires_at > utcnow()


class AccountRecoveryCode(db.Model):
    """HR-assisted secure recovery code for members unable to access registered email."""

    __tablename__ = "account_recovery_codes"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    issued_by_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    code_hash = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    organization = db.relationship("Organization")
    user = db.relationship("User", foreign_keys=[user_id])
    issued_by = db.relationship("User", foreign_keys=[issued_by_id])

    @property
    def is_valid(self) -> bool:
        return self.used_at is None and self.expires_at > utcnow()


class OrganizationSubscription(db.Model, TimestampMixin):
    """Enterprise training commercial subscription."""

    __tablename__ = "organization_subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    plan_code = db.Column(db.String(32), default=PLAN_STARTER, nullable=False)
    plan_name = db.Column(db.String(64), default="Starter Academy", nullable=False)
    seats_limit = db.Column(db.Integer, default=50, nullable=False)
    billing_cycle = db.Column(db.String(20), default="annual", nullable=False)
    price_cents = db.Column(db.Integer, default=60000, nullable=False)
    status = db.Column(db.String(32), default="active", nullable=False)  # active, past_due, canceled, expired
    current_period_start = db.Column(db.DateTime, default=utcnow, nullable=False)
    current_period_end = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(64), default="invoice")
    last_payment_at = db.Column(db.DateTime)
    last_payment_reference = db.Column(db.String(128))

    organization = db.relationship("Organization", back_populates="subscriptions")


class SubscriptionInvoice(db.Model, TimestampMixin):
    """Invoices and payment records for organization subscriptions."""

    __tablename__ = "subscription_invoices"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    invoice_number = db.Column(db.String(64), unique=True, nullable=False)
    amount_cents = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(8), default="USD", nullable=False)
    status = db.Column(db.String(32), default="paid", nullable=False)  # paid, pending, failed, refunded
    pdf_url = db.Column(db.String(255))
    paid_at = db.Column(db.DateTime)

    organization = db.relationship("Organization", back_populates="invoices")
