"""Progress, gamification, assessment, certificate and audit models."""

from datetime import date

from app.extensions import db
from app.models.user import TimestampMixin, utcnow

# Activity types tracked by UserProgress / LearningEvent.
ITEM_TYPES = ("video", "comic", "lab", "game", "lesson", "module", "path", "assessment", "challenge")

CERTIFICATE_TIERS = {
    "basic": {"name": "CyberQuest Basic", "required_labs": 30, "xp": 500},
    "intermediate": {"name": "CyberQuest Intermediate", "required_labs": 60, "xp": 1500},
    "advanced": {"name": "CyberQuest Advanced", "required_labs": 90, "xp": 3000},
    "master": {"name": "CyberQuest Master", "required_labs": 100, "xp": 5000},
}


class UserProgress(db.Model, TimestampMixin):
    """Per-user state for one content item.

    A degraded copy of the truth is never trusted: completion is derived from
    validated attempts / activity events where available.
    """

    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    item_type = db.Column(db.String(24), nullable=False, index=True)
    item_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(24), default="not_started", nullable=False)
    # not_started | in_progress | completed
    progress_percent = db.Column(db.Integer, default=0, nullable=False)
    best_score = db.Column(db.Integer, default=0, nullable=False)
    attempts_count = db.Column(db.Integer, default=0, nullable=False)
    hints_used = db.Column(db.Integer, default=0, nullable=False)
    time_spent_seconds = db.Column(db.Integer, default=0, nullable=False)
    first_attempt_passed = db.Column(db.Boolean)
    last_position_seconds = db.Column(db.Integer, default=0, nullable=False)
    completed_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="progress_records")

    __table_args__ = (
        db.UniqueConstraint("user_id", "item_type", "item_id", name="uq_progress_item"),
        db.Index("ix_progress_user_type", "user_id", "item_type"),
    )


class XPTransaction(db.Model):
    """Immutable XP ledger.

    The unique constraint guarantees a qualifying event can never award XP
    twice, which blocks replay farming (see specification section 11).
    """

    __tablename__ = "xp_transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(64), nullable=False)
    reference_type = db.Column(db.String(32), nullable=False, default="")
    reference_id = db.Column(db.String(64), nullable=False, default="")
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)

    user = db.relationship("User", back_populates="xp_transactions")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "reason", "reference_type", "reference_id", name="uq_xp_event"
        ),
    )


class StreakDay(db.Model):
    __tablename__ = "streak_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    day = db.Column(db.Date, nullable=False, default=date.today)
    qualified = db.Column(db.Boolean, default=False, nullable=False)
    activity_count = db.Column(db.Integer, default=0, nullable=False)
    xp_earned = db.Column(db.Integer, default=0, nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "day", name="uq_streak_day"),)


class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name_en = db.Column(db.String(120), nullable=False)
    name_hi = db.Column(db.String(120))
    description_en = db.Column(db.Text)
    description_hi = db.Column(db.Text)
    icon = db.Column(db.String(32), default="star")
    # criteria_type: labs_completed | perfect_score | streak | certificate_tier
    #                | videos_completed | games_completed | no_hint_labs
    criteria_type = db.Column(db.String(40), nullable=False)
    criteria_value = db.Column(db.Integer, default=1, nullable=False)
    criteria_extra = db.Column(db.String(64))
    xp_bonus = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    awards = db.relationship("UserAchievement", back_populates="achievement")


class UserAchievement(db.Model):
    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False)
    awarded_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    achievement = db.relationship("Achievement", back_populates="awards")

    __table_args__ = (db.UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),)


class AssessmentAttempt(db.Model):
    __tablename__ = "assessment_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = db.Column(db.String(120), nullable=False, index=True)
    phase = db.Column(db.String(24), nullable=False, default="knowledge_check")
    # baseline | post | retention | knowledge_check | certificate
    score = db.Column(db.Integer, default=0, nullable=False)
    max_score = db.Column(db.Integer, default=0, nullable=False)
    percentage = db.Column(db.Integer, default=0, nullable=False)
    passed = db.Column(db.Boolean, default=False, nullable=False)
    answers_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)


class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    certificate_uid = db.Column(db.String(40), unique=True, nullable=False, index=True)
    verification_code = db.Column(db.String(24), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tier = db.Column(db.String(24), nullable=False)
    learner_name = db.Column(db.String(160), nullable=False)
    score_percentage = db.Column(db.Integer, default=0, nullable=False)
    labs_completed = db.Column(db.Integer, default=0, nullable=False)
    issued_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    issued_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    revoked = db.Column(db.Boolean, default=False, nullable=False)
    revoked_reason = db.Column(db.String(255))

    user = db.relationship("User", foreign_keys=[user_id])

    __table_args__ = (db.UniqueConstraint("user_id", "tier", name="uq_certificate_tier_per_user"),)


class LearningEvent(db.Model):
    """Raw, append-only analytics event stream."""

    __tablename__ = "learning_analytics"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = db.Column(db.String(48), nullable=False, index=True)
    item_type = db.Column(db.String(24))
    item_id = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer, default=0, nullable=False)
    success = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    payload_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)

    __table_args__ = (db.Index("ix_event_user_created", "user_id", "created_at"),)


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_hi = db.Column(db.String(200))
    body_en = db.Column(db.Text)
    body_hi = db.Column(db.Text)
    kind = db.Column(db.String(32), default="info", nullable=False)
    link = db.Column(db.String(300))
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)


class AuditLog(db.Model):
    """Significant administrative and security-relevant actions.

    Never store passwords, session tokens or unnecessary personal data here.
    """

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    action = db.Column(db.String(64), nullable=False, index=True)
    target_type = db.Column(db.String(48))
    target_id = db.Column(db.String(64))
    detail_json = db.Column(db.Text)
    ip_address = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False, index=True)
