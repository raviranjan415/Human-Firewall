"""Database models for Human Firewall.

Importing this package exposes every model so that `db.create_all()` and
Flask-Migrate can discover the full schema.
"""

from app.models.user import (  # noqa: F401
    GroupMembership,
    LearningAssignment,
    Role,
    User,
    UserPreference,
)
from app.models.organization import (  # noqa: F401
    AccountRecoveryCode,
    EligibleMember,
    EmailVerificationToken,
    OrgInvitation,
    Organization,
    OrganizationMembership,
    OrganizationSubscription,
    PasswordResetToken,
    SubscriptionInvoice,
)
from app.models.content import (  # noqa: F401
    Comic,
    ComicPanel,
    Game,
    GameScenario,
    LearningPath,
    Lesson,
    Module,
    Question,
    ScenarioChoice,
    VideoAsset,
    VideoLanguageTrack,
)
from app.models.labs import Lab, LabAttempt, LabPrerequisite  # noqa: F401
from app.models.progress import (  # noqa: F401
    Achievement,
    AssessmentAttempt,
    AuditLog,
    Certificate,
    LearningEvent,
    Notification,
    StreakDay,
    UserAchievement,
    UserProgress,
    XPTransaction,
)
from app.models.intel import (  # noqa: F401
    CommunityPost,
    CyberNews,
    HistoricalIncident,
    IncidentSource,
    ModerationReport,
    NewsSource,
)

__all__ = [
    "Role",
    "User",
    "UserPreference",
    "Organization",
    "OrganizationMembership",
    "EligibleMember",
    "OrgInvitation",
    "EmailVerificationToken",
    "PasswordResetToken",
    "AccountRecoveryCode",
    "OrganizationSubscription",
    "SubscriptionInvoice",
    "GroupMembership",
    "LearningAssignment",
    "LearningPath",
    "Module",
    "Lesson",
    "VideoAsset",
    "VideoLanguageTrack",
    "Comic",
    "ComicPanel",
    "Game",
    "GameScenario",
    "ScenarioChoice",
    "Question",
    "Lab",
    "LabPrerequisite",
    "LabAttempt",
    "UserProgress",
    "XPTransaction",
    "StreakDay",
    "Achievement",
    "AssessmentAttempt",
    "UserAchievement",
    "Certificate",
    "LearningEvent",
    "Notification",
    "AuditLog",
    "HistoricalIncident",
    "IncidentSource",
    "CyberNews",
    "NewsSource",
    "CommunityPost",
    "ModerationReport",
]

