"""Authentication and settings forms with server-side validation."""

import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    Regexp,
    ValidationError,
)

from app.models import User

PASSWORD_MESSAGE = (
    "Password must be at least 10 characters and include a letter and a number."
)


def password_strength(form, field):
    value = field.data or ""
    if len(value) < 10 or not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
        raise ValidationError(PASSWORD_MESSAGE)


class RegistrationForm(FlaskForm):
    username = StringField(
        "auth.username",
        validators=[
            DataRequired(),
            Length(min=3, max=64),
            Regexp(r"^[A-Za-z0-9_.-]+$", message="Use letters, numbers, dot, dash or underscore."),
        ],
    )
    email = StringField("auth.email", validators=[DataRequired(), Email(), Length(max=255)])
    display_name = StringField("auth.display_name", validators=[Optional(), Length(max=120)])
    password = PasswordField("auth.password", validators=[DataRequired(), password_strength])
    confirm_password = PasswordField(
        "auth.confirm_password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    accept_terms = BooleanField("auth.accept_terms", validators=[DataRequired()])
    submit = SubmitField("nav.register")

    def validate_username(self, field):
        if User.query.filter(func_lower(User.username) == field.data.lower()).first():
            raise ValidationError("That username is already taken.")

    def validate_email(self, field):
        if User.query.filter(func_lower(User.email) == field.data.lower()).first():
            raise ValidationError("An account with that email already exists.")


class OrgEnrollmentForm(FlaskForm):
    """Organization student or employee registration and enrollment form."""

    display_name = StringField("auth.display_name", validators=[Optional(), Length(max=120)])
    username = StringField(
        "auth.username",
        validators=[
            DataRequired(),
            Length(min=3, max=64),
            Regexp(r"^[A-Za-z0-9_.-]+$", message="Use letters, numbers, dot, dash or underscore."),
        ],
    )
    email = StringField("auth.email", validators=[DataRequired(), Email(), Length(max=255)])
    org_code = StringField("Organization Code", validators=[DataRequired(), Length(max=32)])
    registration_id = StringField("Registration ID / Employee ID", validators=[DataRequired(), Length(max=120)])
    passcode = PasswordField("Enrollment Passcode (if required)", validators=[Optional(), Length(max=120)])
    password = PasswordField("auth.password", validators=[DataRequired(), password_strength])
    confirm_password = PasswordField(
        "auth.confirm_password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    accept_terms = BooleanField("auth.accept_terms", validators=[DataRequired()])
    submit = SubmitField("Join Organization Workspace")

    def validate_username(self, field):
        if User.query.filter(func_lower(User.username) == field.data.lower()).first():
            raise ValidationError("That username is already taken.")

    def validate_email(self, field):
        if User.query.filter(func_lower(User.email) == field.data.lower()).first():
            raise ValidationError("An account with that email already exists. Sign in to link your organization.")


class JoinOrgForm(FlaskForm):
    """Logged-in personal learners linking an authorized organization workspace."""

    org_code = StringField("Organization Code", validators=[DataRequired(), Length(max=32)])
    registration_id = StringField("Registration ID / Employee ID", validators=[DataRequired(), Length(max=120)])
    passcode = PasswordField("Enrollment Passcode (if required)", validators=[Optional(), Length(max=120)])
    submit = SubmitField("Verify Eligibility & Join Workspace")


class RecoveryRedeemForm(FlaskForm):
    """Redeem HR-assisted recovery code to set a new password."""

    recovery_code = StringField("HR Recovery Code", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("New Password", validators=[DataRequired(), password_strength])
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Set New Password & Sign In")


def func_lower(column):
    from sqlalchemy import func

    return func.lower(column)


class LoginForm(FlaskForm):
    # Accepts either a username or an email address.
    identifier = StringField("auth.username", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("auth.password", validators=[DataRequired()])
    remember = BooleanField("auth.remember")
    submit = SubmitField("nav.login")


class ResetRequestForm(FlaskForm):
    email = StringField("auth.email", validators=[DataRequired(), Email()])
    submit = SubmitField("auth.reset_send")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("auth.reset_new", validators=[DataRequired(), password_strength])
    confirm_password = PasswordField(
        "auth.confirm_password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("auth.reset_new")


class SettingsForm(FlaskForm):
    display_name = StringField("auth.display_name", validators=[Optional(), Length(max=120)])
    locale = SelectField("nav.language", choices=[("en", "English"), ("hi", "हिन्दी")])
    timezone = StringField("timezone", validators=[Optional(), Length(max=64)])
    learning_mode = SelectField(
        "learning_mode",
        choices=[("explorer", "Explorer"), ("challenge", "Challenge"), ("professional", "Professional")],
    )
    text_size = SelectField(
        "text_size",
        choices=[("normal", "Normal"), ("large", "Large"), ("xlarge", "Extra large")],
    )
    reduce_motion = BooleanField("reduce_motion")
    high_contrast = BooleanField("high_contrast")
    email_notifications = BooleanField("email_notifications")
    public_leaderboard = BooleanField("public_leaderboard")
    submit = SubmitField("nav.settings")

