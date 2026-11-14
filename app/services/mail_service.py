"""Email dispatch service for password resets, security notifications, and alerts.

Supports standard SMTP configuration via environment variables:
- MAIL_SERVER (e.g. smtp.gmail.com, email-smtp.us-east-1.amazonaws.com)
- MAIL_PORT (e.g. 587 or 465)
- MAIL_USERNAME
- MAIL_PASSWORD
- MAIL_USE_TLS (default True)
- MAIL_DEFAULT_SENDER (default no-reply@humanfirewall.io)

Gracefully falls back to structured logging when SMTP is not configured.
"""

from __future__ import annotations

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, text_body: str, html_body: str | None = None) -> bool:
    """Send an email using configured SMTP settings or log gracefully."""
    mail_server = os.environ.get("MAIL_SERVER") or current_app.config.get("MAIL_SERVER")
    mail_port = int(os.environ.get("MAIL_PORT") or current_app.config.get("MAIL_PORT", 587))
    mail_username = os.environ.get("MAIL_USERNAME") or current_app.config.get("MAIL_USERNAME")
    mail_password = os.environ.get("MAIL_PASSWORD") or current_app.config.get("MAIL_PASSWORD")
    mail_use_tls = os.environ.get("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
    default_sender = (
        os.environ.get("MAIL_DEFAULT_SENDER")
        or current_app.config.get("MAIL_DEFAULT_SENDER")
        or "no-reply@humanfirewall.io"
    )

    if not mail_server or not mail_username:
        logger.info(
            "[MAIL DISPATCH - LOCAL/DEV] To: %s | Subject: %s | Body preview: %s",
            to_email,
            subject,
            text_body[:120].replace("\n", " "),
        )
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = default_sender
        msg["To"] = to_email

        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        if html_body:
            msg.attach(MIMEText(html_body, "html", "utf-8"))

        if mail_port == 465:
            with smtplib.SMTP_SSL(mail_server, mail_port, timeout=10) as server:
                server.login(mail_username, mail_password)
                server.sendmail(default_sender, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(mail_server, mail_port, timeout=10) as server:
                if mail_use_tls:
                    server.starttls()
                server.login(mail_username, mail_password)
                server.sendmail(default_sender, [to_email], msg.as_string())

        logger.info("Successfully sent email to %s (Subject: %s)", to_email, subject)
        return True
    except Exception as exc:
        logger.error("Failed to deliver email to %s via %s: %s", to_email, mail_server, exc)
        return False


def send_password_reset_email(user, reset_url: str) -> bool:
    """Send a secure password reset email with clear verification instructions."""
    subject = "Reset Your Human Firewall Password"
    user_name = user.display_name or user.username or "Learner"

    text_body = f"""Hello {user_name},

We received a request to reset the password for your Human Firewall account ({user.email}).

Click the secure link below to choose a new password:
{reset_url}

This link is valid for 30 minutes and can only be used once.

If you did not request this password reset, please ignore this email or notify your organization's security team immediately. Your account remains secure.

Best regards,
The Human Firewall Security Team
"""

    html_body = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 24px; }}
    .container {{ max-width: 540px; margin: 0 auto; background-color: #1e293b; border-radius: 12px; padding: 32px; border: 1px solid #334155; }}
    .logo {{ color: #38bdf8; font-size: 22px; font-weight: bold; margin-bottom: 24px; }}
    .btn {{ display: inline-block; background-color: #2563eb; color: #ffffff !important; text-decoration: none; padding: 12px 28px; border-radius: 8px; font-weight: bold; margin: 24px 0; }}
    .footer {{ margin-top: 32px; font-size: 12px; color: #94a3b8; border-top: 1px solid #334155; padding-top: 16px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">🛡️ Human Firewall</div>
    <h2 style="color: #ffffff; margin-top: 0;">Password Reset Instructions</h2>
    <p>Hello <strong>{user_name}</strong>,</p>
    <p>We received a request to reset the password for your account associated with <strong>{user.email}</strong>.</p>
    <div style="text-align: center;">
      <a href="{reset_url}" class="btn">Reset My Password &rarr;</a>
    </div>
    <p style="font-size: 13px; color: #94a3b8;">
      If the button above does not work, copy and paste this URL into your browser:<br>
      <a href="{reset_url}" style="color: #38bdf8; word-break: break-all;">{reset_url}</a>
    </p>
    <p style="font-size: 13px; color: #cbd5e1;">
      ⚠️ <em>This single-use link is valid for 30 minutes. If you did not initiate this request, no action is required and your account remains protected.</em>
    </p>
    <div class="footer">
      Human Firewall Cyber Defense Platform &bull; Automated Security Dispatch
    </div>
  </div>
</body>
</html>
"""
    return send_email(user.email, subject, text_body, html_body)
