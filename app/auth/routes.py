"""Authentication routes: personal learning, organization enrollment, recovery, and settings."""

from __future__ import annotations

import logging
from datetime import timedelta

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.auth.forms import (
    JoinOrgForm,
    LoginForm,
    OrgEnrollmentForm,
    RecoveryRedeemForm,
    RegistrationForm,
    ResetPasswordForm,
    ResetRequestForm,
    SettingsForm,
)
from app.extensions import db, limiter
from app.models import Organization, OrganizationMembership, User, UserAchievement, UserPreference
from app.models.user import ROLE_LEARNER, Role, utcnow
from app.services.auth_tokens import (
    consume_password_reset_token,
    create_email_verification_token,
    create_password_reset_token,
    validate_password_reset_token,
    verify_email_token,
)
from app.services.organizations import (
    redeem_recovery_code,
    verify_and_enroll_member,
)

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)

MAX_FAILED_LOGINS = 5
LOCKOUT_MINUTES = 15
RESET_TOKEN_MAX_AGE = 30 * 60  # 30 minutes


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="password-reset")


def _dashboard_redirect():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if current_user.is_admin:
        return redirect(url_for("admin.index"))
    if current_user.is_org_admin:
        active_org = current_user.active_organization
        if active_org:
            return redirect(url_for("organization.workspace_overview", org_id=active_org.id))
    return redirect(url_for("dashboard.index"))


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("20 per hour")
def register():
    """Personal Learning registration — no organization required."""
    if current_user.is_authenticated:
        return _dashboard_redirect()

    form = RegistrationForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name=ROLE_LEARNER).first()
        if role is None:
            flash("Registration is temporarily unavailable.", "error")
            return render_template("auth/register.html", form=form)

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            display_name=(form.display_name.data or "").strip() or form.username.data.strip(),
            role_id=role.id,
            locale=session.get("locale", current_app.config["DEFAULT_LOCALE"]),
            email_verified=False,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        db.session.add(UserPreference(user_id=user.id, language=user.locale))
        db.session.commit()

        # Generate single-use email verification token
        verification_token = create_email_verification_token(user)
        if current_app.debug:
            logger.info("Email verification link: %s", url_for("auth.verify_email", token=verification_token, _external=True))

        session.clear()
        login_user(user, remember=False)
        session.permanent = True
        flash("auth.account_created", "success")
        return _dashboard_redirect()

    return render_template("auth/register.html", form=form)


@auth_bp.route("/enroll", methods=["GET", "POST"])
@limiter.limit("20 per hour")
def enroll():
    """Organization student or employee registration and enrollment with Reg ID verification."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.join_org"))

    form = OrgEnrollmentForm()
    # Pre-fill organization code if provided via query string
    if request.method == "GET" and request.args.get("code"):
        form.org_code.data = request.args.get("code").strip().upper()

    if form.validate_on_submit():
        role = Role.query.filter_by(name=ROLE_LEARNER).first()
        if role is None:
            flash("Registration is temporarily unavailable.", "error")
            return render_template("auth/enroll.html", form=form)

        # 1. Create account first
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            display_name=(form.display_name.data or "").strip(),
            role_id=role.id,
            locale=session.get("locale", current_app.config["DEFAULT_LOCALE"]),
            email_verified=False,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        db.session.add(UserPreference(user_id=user.id, language=user.locale))
        db.session.commit()

        # 2. Run automated eligibility verification engine
        result = verify_and_enroll_member(
            org_code=form.org_code.data,
            registration_id=form.registration_id.data,
            user=user,
            passcode=form.passcode.data,
        )

        if not result["success"]:
            # Rollback user creation if verification fails
            db.session.delete(user)
            db.session.commit()
            flash(result["error"], "error")
            return render_template("auth/enroll.html", form=form)

        # Generate single-use email verification token
        create_email_verification_token(user)

        session.clear()
        login_user(user, remember=False)
        session.permanent = True
        flash(result["message"], "success")
        return _dashboard_redirect()

    return render_template("auth/enroll.html", form=form)


@auth_bp.route("/join-org", methods=["GET", "POST"])
@login_required
def join_org():
    """Allow an existing personal user to join an organization workspace without duplicating their account."""
    form = JoinOrgForm()
    if request.method == "GET" and request.args.get("code"):
        form.org_code.data = request.args.get("code").strip().upper()

    if form.validate_on_submit():
        result = verify_and_enroll_member(
            org_code=form.org_code.data,
            registration_id=form.registration_id.data,
            user=current_user,
            passcode=form.passcode.data,
        )
        if result["success"]:
            flash(result["message"], "success")
            return _dashboard_redirect()
        else:
            flash(result["error"], "error")

    return render_template("auth/join_org.html", form=form)


@auth_bp.route("/switch-workspace/<int:org_id>", methods=["POST"])
@login_required
def switch_workspace(org_id: int):
    """Switch active workspace for users belonging to multiple organizations."""
    membership = current_user.get_membership(org_id)
    if not membership or membership.status != "active":
        flash("You are not an active member of that workspace.", "error")
        return redirect(url_for("dashboard.index"))

    current_user.organization_id = org_id
    db.session.commit()
    flash(f"Switched active workspace to {membership.organization.name}.", "success")
    return _dashboard_redirect()


@auth_bp.route("/verify-email/<token>", methods=["GET"])
def verify_email(token: str):
    """Verify email address with cryptographic single-use token."""
    success, message, user = verify_email_token(token)
    if success:
        flash(message, "success")
        if not current_user.is_authenticated and user:
            login_user(user)
        return _dashboard_redirect()
    else:
        flash(message, "error")
        return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit(lambda: current_app.config.get("LOGIN_RATE_LIMIT", "10 per minute"))
def login():
    if current_user.is_authenticated:
        return _dashboard_redirect()

    # Track login context: 'personal', 'org', or 'admin'
    login_context = request.args.get("type", "personal")
    prefill_code = request.args.get("code", "")

    form = LoginForm()
    if form.validate_on_submit():
        identifier = (form.identifier.data or "").strip().lower()
        user = User.query.filter(
            db.or_(db.func.lower(User.username) == identifier,
                   db.func.lower(User.email) == identifier)
        ).first()

        if user and user.locked_until and user.locked_until > utcnow():
            flash("Account temporarily locked after repeated failed attempts.", "error")
            return render_template("auth/login.html", form=form, login_context=login_context, prefill_code=prefill_code)

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash("This account is disabled. Contact an administrator.", "error")
                return render_template("auth/login.html", form=form, login_context=login_context, prefill_code=prefill_code)

            user.failed_login_count = 0
            user.locked_until = None
            user.last_login_at = utcnow()
            db.session.commit()

            session.clear()
            login_user(user, remember=bool(form.remember.data))
            session.permanent = True
            if user.preference:
                session["locale"] = user.preference.language
            return _dashboard_redirect()

        # Failed attempt — rate limiting and lockout without enumeration
        if user:
            user.failed_login_count = (user.failed_login_count or 0) + 1
            if user.failed_login_count >= MAX_FAILED_LOGINS:
                user.locked_until = utcnow() + timedelta(minutes=LOCKOUT_MINUTES)
                user.failed_login_count = 0
            db.session.commit()

        flash("Invalid credentials. Please try again.", "error")

    return render_template("auth/login.html", form=form, login_context=login_context, prefill_code=prefill_code)


@auth_bp.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("auth.logged_out", "info")
    return redirect(url_for("public.landing"))


@auth_bp.route("/forgot", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def forgot_password():
    form = ResetRequestForm()
    reset_link = None
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter(db.func.lower(User.email) == email).first()
        if user is not None and user.is_active:
            token = create_password_reset_token(user)
            reset_link = url_for("auth.reset_password", token=token, _external=True)
            logger.info("Password reset requested for user id %s", user.id)
            if not current_app.debug:
                reset_link = None

        # Anti-enumeration response
        flash("If that account exists, reset instructions have been created.", "info")

    return render_template("auth/forgot.html", form=form, reset_link=reset_link)


@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token: str):
    """Reset password with single-use token consumption preventing replay attacks."""
    is_valid, user, token_record = validate_password_reset_token(token)
    legacy_uid = None

    if not is_valid:
        # Fallback to itsdangerous legacy token for backward compatibility
        try:
            payload = _serializer().loads(token, max_age=RESET_TOKEN_MAX_AGE)
            legacy_uid = payload.get("uid")
            user = db.session.get(User, legacy_uid)
            if user and user.is_active:
                is_valid = True
        except (BadSignature, SignatureExpired):
            pass

    if not is_valid or not user:
        flash("That reset link is not valid or has expired. Please request a new one.", "error")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        if token_record:
            consume_password_reset_token(token_record, form.password.data)
        else:
            user.set_password(form.password.data)
            user.failed_login_count = 0
            user.locked_until = None
            db.session.commit()

        flash("Password updated successfully. You can sign in now.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset.html", form=form)


@auth_bp.route("/recover", methods=["GET", "POST"])
def recover():
    """Public portal to redeem an HR-assisted recovery code."""
    form = RecoveryRedeemForm()
    if form.validate_on_submit():
        success, message = redeem_recovery_code(
            form.recovery_code.data, form.password.data
        )
        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))
        else:
            flash(message, "error")

    return render_template("auth/recover.html", form=form)


@auth_bp.route("/profile")
@login_required
def profile():
    from app.services import gamification
    from app.services import progress as progress_service

    achievements = (
        UserAchievement.query.filter_by(user_id=current_user.id)
        .order_by(UserAchievement.awarded_at.desc())
        .all()
    )
    memberships = OrganizationMembership.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "auth/profile.html",
        stats=progress_service.summary(current_user),
        achievements=achievements,
        level_info=gamification.level_progress(current_user.xp_total or 0),
        xp_breakdown=gamification.xp_breakdown(current_user.id),
        memberships=memberships,
    )


@auth_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    preference = current_user.preference
    if preference is None:
        preference = UserPreference(user_id=current_user.id)
        db.session.add(preference)
        db.session.commit()

    form = SettingsForm(obj=preference)
    if request.method == "GET":
        form.locale.data = preference.language
        form.learning_mode.data = current_user.learning_mode
        form.display_name.data = current_user.display_name
        form.timezone.data = current_user.timezone

    if form.validate_on_submit():
        current_user.display_name = (form.display_name.data or "").strip() or current_user.username
        current_user.timezone = (form.timezone.data or "Asia/Kolkata").strip()
        current_user.learning_mode = form.learning_mode.data
        current_user.locale = form.locale.data

        preference.language = form.locale.data
        preference.text_size = form.text_size.data
        preference.reduce_motion = bool(form.reduce_motion.data)
        preference.high_contrast = bool(form.high_contrast.data)
        preference.email_notifications = bool(form.email_notifications.data)
        preference.public_leaderboard = bool(form.public_leaderboard.data)
        db.session.commit()

        session["locale"] = preference.language
        flash("Settings saved.", "success")
        return redirect(url_for("auth.settings"))

    return render_template("auth/settings.html", form=form)

