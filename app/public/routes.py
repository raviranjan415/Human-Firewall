"""Public pages: landing, legal, accessibility and help."""

from flask import Blueprint, redirect, render_template, request, session

from app.extensions import db
from app.models import Comic, Game, HistoricalIncident, Lab, Lesson

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def landing():
    return render_template(
        "public/landing.html",
        stats={
            "labs": Lab.query.filter_by(state="published").count(),
            "video_lessons": Lesson.query.filter_by(state="published").count(),
            "comics": Comic.query.filter_by(state="published").count(),
            "games": Game.query.filter_by(state="published").count(),
            "incidents": HistoricalIncident.query.filter_by(state="published").count(),
        },
    )


@public_bp.route("/lang/<code>")
def set_language(code: str):
    """Switch language without losing progress (nothing else is stored)."""
    from flask import current_app

    if code in current_app.config.get("SUPPORTED_LOCALES", ("en", "hi")):
        session["locale"] = code
    target = request.referrer or "/"
    return redirect(target)


@public_bp.route("/privacy")
def privacy():
    return render_template("public/privacy.html")


@public_bp.route("/about")
def about():
    return render_template("public/about.html")


@public_bp.route("/terms")
def terms():
    return render_template("public/terms.html")


@public_bp.route("/accessibility")
def accessibility():
    return render_template("public/accessibility.html")


@public_bp.route("/help")
def help():
    return render_template("public/help.html")


# Convenience Route Aliases for intuitive top-level navigation
@public_bp.route("/leaderboard")
@public_bp.route("/leaderboard/")
def leaderboard_alias():
    return redirect("/dashboard/leaderboard", code=302)


@public_bp.route("/achievements")
@public_bp.route("/achievements/")
def achievements_alias():
    return redirect("/dashboard/achievements", code=302)


@public_bp.route("/profile")
@public_bp.route("/profile/")
def profile_alias():
    return redirect("/auth/profile", code=302)


@public_bp.route("/org")
@public_bp.route("/org/")
def org_alias():
    return redirect("/org/enterprise", code=302)


@public_bp.route("/healthz")
def healthz():
    from sqlalchemy import text

    try:
        db.session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:  # pragma: no cover - monitoring path
        db_ok = False
    return {
        "status": "ok" if db_ok else "degraded",
        "database": db_ok,
        "service": "human-firewall",
    }


@public_bp.route("/readyz")
def readyz():
    from sqlalchemy import text

    try:
        db.session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}, 200
    except Exception as exc:
        return {"status": "not_ready", "error": str(exc)}, 503


@public_bp.route("/metrics")
def metrics():
    """Prometheus exposition format endpoint."""
    import psutil
    from flask import Response
    from sqlalchemy import text

    from app.models import Game, Lab, User

    try:
        db.session.execute(text("SELECT 1"))
        db_status = 1
    except Exception:
        db_status = 0

    try:
        user_count = User.query.count()
        game_count = Game.query.filter_by(state="published").count()
        lab_count = Lab.query.filter_by(state="published").count()
    except Exception:
        user_count = game_count = lab_count = 0

    cpu_usage = psutil.cpu_percent(interval=None)
    mem_usage = psutil.virtual_memory().percent

    lines = [
        "# HELP human_firewall_database_status Database connectivity (1 = connected, 0 = down)",
        "# TYPE human_firewall_database_status gauge",
        f"human_firewall_database_status {db_status}",
        "# HELP human_firewall_users_total Total registered users on platform",
        "# TYPE human_firewall_users_total counter",
        f"human_firewall_users_total {user_count}",
        "# HELP human_firewall_games_published Total published games",
        "# TYPE human_firewall_games_published gauge",
        f"human_firewall_games_published {game_count}",
        "# HELP human_firewall_labs_published Total published practical labs",
        "# TYPE human_firewall_labs_published gauge",
        f"human_firewall_labs_published {lab_count}",
        "# HELP human_firewall_system_cpu_percent Host CPU utilization percentage",
        "# TYPE human_firewall_system_cpu_percent gauge",
        f"human_firewall_system_cpu_percent {cpu_usage}",
        "# HELP human_firewall_system_memory_percent Host memory utilization percentage",
        "# TYPE human_firewall_system_memory_percent gauge",
        f"human_firewall_system_memory_percent {mem_usage}",
        "",
    ]
    return Response(
        "\n".join(lines), mimetype="text/plain; version=0.0.4; charset=utf-8"
    )
