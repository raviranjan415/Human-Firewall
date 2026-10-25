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


@public_bp.route("/healthz")
def healthz():
    from sqlalchemy import text

    try:
        db.session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:  # pragma: no cover - monitoring path
        db_ok = False
    return {"status": "ok" if db_ok else "degraded", "database": db_ok}
