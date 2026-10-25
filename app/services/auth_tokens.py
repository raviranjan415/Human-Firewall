"""Cryptographic token management for single-use email verification and password resets."""

from __future__ import annotations

import logging
import secrets
from datetime import timedelta

from app.extensions import db
from app.models import AuditLog, EmailVerificationToken, PasswordResetToken, User
from app.models.organization import hash_token
from app.models.user import utcnow

logger = logging.getLogger(__name__)

EMAIL_VERIFICATION_EXPIRES_HOURS = 48
PASSWORD_RESET_EXPIRES_MINUTES = 30


def create_email_verification_token(user: User) -> str:
    """Generate a single-use email verification token."""
    # Clean up previous unused tokens
    EmailVerificationToken.query.filter_by(user_id=user.id, used_at=None).delete()

    raw_token = secrets.token_urlsafe(32)
    token = EmailVerificationToken(
        user_id=user.id,
        token_hash=hash_token(raw_token),
        expires_at=utcnow() + timedelta(hours=EMAIL_VERIFICATION_EXPIRES_HOURS),
    )
    db.session.add(token)
    db.session.commit()
    return raw_token


def verify_email_token(raw_token: str) -> tuple[bool, str, User | None]:
    """Verify and consume an email verification token."""
    clean = (raw_token or "").strip()
    if not clean:
        return False, "Verification token is required.", None

    token_h = hash_token(clean)
    record = EmailVerificationToken.query.filter_by(token_hash=token_h).first()
    if not record or not record.is_valid:
        return False, "Verification link is invalid or has expired.", None

    user = record.user
    if not user:
        return False, "Associated user account was not found.", None

    user.email_verified = True
    record.used_at = utcnow()

    db.session.add(
        AuditLog(
            actor_id=user.id,
            action="email_verified",
            target_type="user",
            target_id=str(user.id),
        )
    )
    db.session.commit()
    return True, "Your email address has been successfully verified.", user


def create_password_reset_token(user: User) -> str:
    """Generate a single-use password reset token."""
    PasswordResetToken.query.filter_by(user_id=user.id, used_at=None).delete()

    raw_token = secrets.token_urlsafe(32)
    token = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_token(raw_token),
        expires_at=utcnow() + timedelta(minutes=PASSWORD_RESET_EXPIRES_MINUTES),
    )
    db.session.add(token)
    db.session.commit()
    return raw_token


def validate_password_reset_token(raw_token: str) -> tuple[bool, User | None, PasswordResetToken | None]:
    """Check validity of a password reset token without consuming it."""
    clean = (raw_token or "").strip()
    if not clean:
        return False, None, None

    token_h = hash_token(clean)
    record = PasswordResetToken.query.filter_by(token_hash=token_h).first()
    if not record or not record.is_valid:
        return False, None, None

    user = record.user
    if not user or not user.is_active:
        return False, None, None

    return True, user, record


def consume_password_reset_token(token_record: PasswordResetToken, new_password: str) -> bool:
    """Consume the password reset token and update the user's password."""
    if not token_record.is_valid:
        return False

    user = token_record.user
    if not user or not user.is_active:
        return False

    user.set_password(new_password)
    user.failed_login_count = 0
    user.locked_until = None
    token_record.used_at = utcnow()

    db.session.add(
        AuditLog(
            actor_id=user.id,
            action="password_reset_completed",
            target_type="user",
            target_id=str(user.id),
        )
    )
    db.session.commit()
    return True
