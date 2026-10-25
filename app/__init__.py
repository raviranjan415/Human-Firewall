"""CyberQuest application factory.

"Motto: Enjoy with Safety — Play Smart, Stay Cyber Safe!"

The factory wires configuration, extensions, blueprints, template helpers,
security headers, error handlers and CLI commands together.
"""

import logging
import os
from pathlib import Path

from flask import Flask, g, jsonify, render_template, request

from app.config import get_config
from app.extensions import csrf, db, limiter, login_manager, migrate

logger = logging.getLogger(__name__)

APP_DIR = Path(__file__).resolve().parent


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(get_config(config_name))

    _ensure_instance_folder(app)
    _configure_logging(app)
    _init_extensions(app)
    _register_blueprints(app)
    _register_template_helpers(app)
    _register_security(app)
    _register_error_handlers(app)
    _register_cli(app)

    from app.services.i18n import init_i18n

    init_i18n(app)

    return app


# ---------------------------------------------------------------------------
# Setup helpers
# ---------------------------------------------------------------------------

def _ensure_instance_folder(app: Flask) -> None:
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)


def _configure_logging(app: Flask) -> None:
    """Structured-ish logging that never records credentials or tokens."""
    if app.testing:
        return
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    )
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO if not app.debug else logging.DEBUG)


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    limiter.enabled = not app.testing
    # Sensitive endpoints get their own decorators; the global default keeps
    # the door shut on runaway clients without punishing normal use.
    if app.config.get("RATELIMIT_ENABLED") is False:
        limiter.enabled = False

    from app import models  # noqa: F401  (register models with SQLAlchemy)
    from app.services import i18n  # noqa: F401


def _register_blueprints(app: Flask) -> None:
    from app.admin.routes import admin_bp
    from app.analytics.routes import analytics_bp
    from app.api.routes import api_bp
    from app.auth.routes import auth_bp
    from app.certificates.routes import certificates_bp
    from app.dashboard.routes import dashboard_bp
    from app.games.routes import games_bp
    from app.incidents.routes import incidents_bp
    from app.labs.routes import labs_bp
    from app.learning.routes import learning_bp
    from app.news.routes import news_bp
    from app.organization.routes import organization_bp
    from app.public.routes import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(organization_bp, url_prefix="/org")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(learning_bp, url_prefix="/learn")
    app.register_blueprint(games_bp, url_prefix="/games")
    app.register_blueprint(labs_bp, url_prefix="/labs")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")
    app.register_blueprint(certificates_bp, url_prefix="/certificates")
    app.register_blueprint(incidents_bp, url_prefix="/what-happened")
    app.register_blueprint(news_bp, url_prefix="/cyber-news")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")


def _register_template_helpers(app: Flask) -> None:
    from app.services.i18n import (
        available_locales,
        current_locale,
        get_theme_classes,
        t,
        t_content,
    )

    app.jinja_env.globals.update(
        t=t,
        t_content=t_content,
        current_locale=current_locale,
        available_locales=available_locales,
        theme_classes=get_theme_classes,
        APP_NAME="Human Firewall",
        TAGLINE_KEY="brand.tagline",
    )

    @app.context_processor
    def inject_globals():
        from flask_login import current_user

        ctx = {"request_path": request.path, "current_user": current_user}
        if current_user.is_authenticated:
            from app.models import Notification

            ctx["unread_notifications"] = (
                Notification.query.filter_by(user_id=current_user.id, is_read=False)
                .order_by(Notification.created_at.desc())
                .limit(5)
                .all()
            )
            ctx["active_org"] = current_user.active_organization
            ctx["joined_orgs"] = current_user.joined_organizations
        else:
            ctx["unread_notifications"] = []
            ctx["active_org"] = None
            ctx["joined_orgs"] = []
        return ctx



def _register_security(app: Flask) -> None:
    @app.after_request
    def apply_security_headers(response):
        for header, value in app.config.get("SECURITY_HEADERS", {}).items():
            response.headers.setdefault(header, value)
        csp = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self' 'unsafe-inline'; "
            "font-src 'self' data:; "
            "media-src 'self' https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers.setdefault("Content-Security-Policy", csp)
        if not app.debug:
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response

    @app.before_request
    def track_request_locale():
        g.locale_requested = request.args.get("lang")


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(error):  # pragma: no cover - template rendering
        if request.path.startswith("/api/"):
            return jsonify({"error": "forbidden", "message": "Not permitted"}), 403
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "not_found", "message": "Resource not found"}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(429)
    def too_many(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "rate_limited", "message": str(error.description)}), 429
        return render_template("errors/429.html", error=error), 429

    @app.errorhandler(500)
    def server_error(error):  # pragma: no cover - defensive
        db.session.rollback()
        app.logger.exception("Unhandled application error")
        if request.path.startswith("/api/"):
            return jsonify({"error": "server_error", "message": "Something went wrong"}), 500
        # Never surface stack traces or internal details to end users.
        return render_template("errors/500.html"), 500


def _register_cli(app: Flask) -> None:
    import click

    @app.cli.command("init-db")
    def init_db():  # pragma: no cover - CLI
        """Create all database tables."""
        db.create_all()
        click.echo("Database tables created.")

    @app.cli.command("seed")
    @click.option("--with-demo/--no-demo", default=None, help="Create demo accounts.")
    def seed(with_demo):  # pragma: no cover - CLI
        """Load roles, bootstrap accounts and sample content."""
        from app.services.seed import run_seed

        summary = run_seed(with_demo=with_demo)
        for line in summary:
            click.echo(line)

    @app.cli.command("reset-db")
    @click.confirmation_option(prompt="This deletes all data. Continue?")
    def reset_db():  # pragma: no cover - CLI
        """Drop and recreate every table, then seed."""
        from app.services.seed import run_seed

        db.drop_all()
        db.create_all()
        for line in run_seed():
            click.echo(line)

    @app.cli.command("ingest-news")
    def ingest_news():  # pragma: no cover - CLI
        """Fetch the latest cyber news from configured RSS sources."""
        from app.services.news_ingest import ingest_all

        for line in ingest_all():
            click.echo(line)

    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.option("--email", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(username, email, password):  # pragma: no cover - CLI
        """Create an administrator account."""
        from app.models import Role, User
        from app.models.user import ROLE_ADMIN

        role = Role.query.filter_by(name=ROLE_ADMIN).first()
        if role is None:
            role = Role(name=ROLE_ADMIN, description="Platform administrator")
            db.session.add(role)
            db.session.flush()
        if User.query.filter(
            (User.username == username) | (User.email == email)
        ).first():
            click.echo("A user with that username or email already exists.")
            return
        user = User(username=username, email=email, display_name=username, role_id=role.id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Administrator '{username}' created.")
