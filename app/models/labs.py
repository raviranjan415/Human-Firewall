"""Practical lab models.

Labs form an ordered pathway (1–100) with strict prerequisite enforcement.
Completion is always validated on the server against the lab's stored
validation configuration — opening a lab never marks it complete.
"""

from app.extensions import db
from app.models.user import TimestampMixin

LAB_LEVELS = ("basic", "intermediate", "advanced", "capstone")


class Lab(db.Model, TimestampMixin):
    __tablename__ = "labs"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False, index=True)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    title_en = db.Column(db.String(240), nullable=False)
    title_hi = db.Column(db.String(240))
    level = db.Column(db.String(24), default="basic", nullable=False, index=True)
    difficulty = db.Column(db.String(24), default="beginner", nullable=False)
    estimated_minutes = db.Column(db.Integer, default=10, nullable=False)

    objectives_en = db.Column(db.Text)
    objectives_hi = db.Column(db.Text)
    scenario_en = db.Column(db.Text)
    scenario_hi = db.Column(db.Text)
    task_en = db.Column(db.Text)
    task_hi = db.Column(db.Text)
    step_by_step_en = db.Column(db.Text)
    step_by_step_hi = db.Column(db.Text)
    remediation_en = db.Column(db.Text)
    remediation_hi = db.Column(db.Text)

    # Interactive task definition -----------------------------------------
    # task_type: "multi_select" | "single_choice" | "order" | "text_judgement"
    task_type = db.Column(db.String(32), default="single_choice", nullable=False)
    options_json = db.Column(db.Text)          # JSON [{id, en, hi}]
    validation_json = db.Column(db.Text)       # JSON {"correct": [...], "min_score": 70}
    hints_json = db.Column(db.Text)            # JSON [{"en":..., "hi":...}]
    payload_json = db.Column(db.Text)          # JSON artefact shown to the learner

    xp_reward = db.Column(db.Integer, default=30, nullable=False)
    pass_score = db.Column(db.Integer, default=70, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    state = db.Column(db.String(24), default="published", nullable=False)

    prerequisites = db.relationship(
        "LabPrerequisite",
        foreign_keys="LabPrerequisite.lab_id",
        back_populates="lab",
        cascade="all, delete-orphan",
    )
    attempts = db.relationship("LabAttempt", back_populates="lab", cascade="all, delete-orphan")

    def prerequisite_ids(self) -> list[int]:
        return [p.requires_lab_id for p in self.prerequisites]

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Lab {self.number} {self.slug}>"


class LabPrerequisite(db.Model):
    __tablename__ = "lab_prerequisites"

    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id", ondelete="CASCADE"), nullable=False, index=True)
    requires_lab_id = db.Column(db.Integer, db.ForeignKey("labs.id", ondelete="CASCADE"), nullable=False)

    lab = db.relationship("Lab", foreign_keys=[lab_id], back_populates="prerequisites")
    requires_lab = db.relationship("Lab", foreign_keys=[requires_lab_id])

    __table_args__ = (db.UniqueConstraint("lab_id", "requires_lab_id", name="uq_lab_prerequisite"),)


class LabAttempt(db.Model, TimestampMixin):
    __tablename__ = "lab_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.id", ondelete="CASCADE"), nullable=False, index=True)

    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Integer, default=0, nullable=False)
    max_score = db.Column(db.Integer, default=100, nullable=False)
    percentage = db.Column(db.Integer, default=0, nullable=False)
    passed = db.Column(db.Boolean, default=False, nullable=False)
    hints_used = db.Column(db.Integer, default=0, nullable=False)
    retry_count = db.Column(db.Integer, default=0, nullable=False)
    time_spent_seconds = db.Column(db.Integer, default=0, nullable=False)
    # Only whether the learner answered correctly is stored — never credentials.
    submitted_json = db.Column(db.Text)
    feedback_en = db.Column(db.Text)
    feedback_hi = db.Column(db.Text)
    status = db.Column(db.String(24), default="in_progress", nullable=False)

    lab = db.relationship("Lab", back_populates="attempts")
    user = db.relationship("User")

    __table_args__ = (
        db.Index("ix_lab_attempt_user_lab", "user_id", "lab_id"),
    )
