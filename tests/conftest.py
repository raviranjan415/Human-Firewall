"""Shared fixtures for the CyberQuest test-suite.

The suite runs against ``TestingConfig``: an in-memory SQLite database with
CSRF and rate limiting disabled, demo accounts off and a known administrator
password. The app is created once per session and seeded once; a function
scoped fixture removes learner-generated rows between tests so the content
catalogue stays intact.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app  # noqa: E402
from app.extensions import db as _db  # noqa: E402
from app.models import (  # noqa: E402
    AuditLog,
    Certificate,
    CyberNews,
    LabAttempt,
    LearningEvent,
    Notification,
    Role,
    StreakDay,
    User,
    UserAchievement,
    UserPreference,
    UserProgress,
    XPTransaction,
    AccountRecoveryCode,
    EligibleMember,
    EmailVerificationToken,
    LearningAssignment,
    OrgInvitation,
    Organization,
    OrganizationMembership,
    OrganizationSubscription,
    PasswordResetToken,
    SubscriptionInvoice,
)
from app.models.user import ROLE_INSTRUCTOR, ROLE_LEARNER  # noqa: E402
from app.services.seed import run_seed  # noqa: E402

# TestingConfig supplies these.
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@150305"
LEARNER_PASSWORD = "Testing1pass"

BASELINE_USERNAMES = (ADMIN_USERNAME,)

USER_DATA_MODELS = (
    SubscriptionInvoice,
    OrganizationSubscription,
    LearningAssignment,
    AccountRecoveryCode,
    PasswordResetToken,
    EmailVerificationToken,
    OrgInvitation,
    EligibleMember,
    OrganizationMembership,
    Organization,
    XPTransaction,
    UserAchievement,
    StreakDay,
    UserProgress,
    LabAttempt,
    Certificate,
    LearningEvent,
    Notification,
    AuditLog,
    CyberNews,
)


@pytest.fixture(scope="session")
def app():
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        run_seed(with_demo=False)
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(autouse=True)
def clean_learner_data(app):
    """Keep the seeded catalogue, drop everything a test creates.

    Tests share a single long-lived application context, so two pieces of
    state have to be reset explicitly:

    * Flask-Login caches the signed-in user on ``g``; left alone, the next
      test would inherit an expired, detached ``User``.
    * Rows are removed with bulk ``DELETE`` statements, which does not evict
      the matching instances from the session's identity map.
    """
    yield
    from flask import g

    g.pop("_login_user", None)

    _db.session.rollback()
    keep_ids = [row.id for row in User.query.filter(User.username.in_(BASELINE_USERNAMES)).all()]
    for model in USER_DATA_MODELS:
        model.query.delete(synchronize_session=False)
    UserPreference.query.filter(~UserPreference.user_id.in_(keep_ids)).delete(
        synchronize_session=False
    )
    User.query.filter(~User.id.in_(keep_ids)).delete(synchronize_session=False)
    _db.session.commit()
    _db.session.expunge_all()
    _db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def make_user(app):
    """Create a user with the given role and return it."""

    def _make(
        username: str = "learner1",
        role: str = ROLE_LEARNER,
        password: str = LEARNER_PASSWORD,
        **kwargs,
    ) -> User:
        role_row = Role.query.filter_by(name=role).first()
        assert role_row is not None, f"role {role} was not seeded"
        user = User(
            username=username,
            email=kwargs.pop("email", f"{username}@example.com"),
            display_name=kwargs.pop("display_name", username),
            role_id=role_row.id,
            email_verified=True,
            **kwargs,
        )
        user.set_password(password)
        _db.session.add(user)
        _db.session.flush()
        _db.session.add(UserPreference(user_id=user.id, language=user.locale or "en"))
        _db.session.commit()
        return user

    return _make


@pytest.fixture
def learner(make_user):
    return make_user("learner1", ROLE_LEARNER)


@pytest.fixture
def instructor(make_user):
    return make_user("instructor1", ROLE_INSTRUCTOR)


@pytest.fixture
def admin_user(app):
    return User.query.filter_by(username=ADMIN_USERNAME).first()


def login(client, identifier: str, password: str = LEARNER_PASSWORD):
    """Log a test client in through the real login view."""
    return client.post(
        "/auth/login",
        data={"identifier": identifier, "password": password},
        follow_redirects=True,
    )


def logout(client):
    return client.post("/auth/logout", follow_redirects=True)


@pytest.fixture
def logged_in(client):
    """Return a helper that logs the given username in."""

    def _login(identifier: str, password: str = LEARNER_PASSWORD):
        return login(client, identifier, password)

    return _login
