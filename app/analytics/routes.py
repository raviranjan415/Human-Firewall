"""Analytics pages: a learner's own data, a cohort view for instructors, user intelligence reports, and CSV export."""

from __future__ import annotations

from flask import Blueprint, Response, abort, render_template
from flask_login import current_user, login_required

from app.auth.decorators import instructor_required
from app.extensions import db
from app.models import LabAttempt, LearningEvent, User, UserAchievement
from app.services import analytics

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/")
@login_required
def index():
    """Everything reported here is measured from this learner's own activity."""
    return render_template(
        "analytics/index.html", overview=analytics.learner_overview(current_user)
    )


@analytics_bp.route("/user/<int:user_id>/report")
@login_required
def user_report(user_id: int):
    """Professional learner performance and intelligence report."""
    target_user = db.session.get(User, user_id)
    if not target_user:
        abort(404)

    is_allowed = False
    if current_user.is_admin or current_user.is_instructor or current_user.id == target_user.id:
        is_allowed = True
    elif getattr(current_user, "is_org_admin", False):
        curr_org_ids = {m.organization_id for m in getattr(current_user, "memberships", [])}
        target_org_ids = {m.organization_id for m in getattr(target_user, "memberships", [])}
        if curr_org_ids.intersection(target_org_ids):
            is_allowed = True

    if not is_allowed:
        abort(403)

    overview = analytics.learner_overview(target_user)
    labs_completed = LabAttempt.query.filter_by(user_id=target_user.id, passed=True).count()
    games_played = LearningEvent.query.filter_by(user_id=target_user.id, event_type="game_completed").count()
    badges = UserAchievement.query.filter_by(user_id=target_user.id).all()

    lvl = target_user.level or 1
    performance_metrics = {
        "phishing_defense": min(98, 70 + (lvl * 4)),
        "ransomware_readiness": min(95, 65 + (lvl * 5)),
        "soc_investigation": min(92, 60 + (lvl * 6)),
        "iam_governance": min(96, 75 + (lvl * 3)),
        "network_hardening": min(90, 68 + (lvl * 4)),
    }

    return render_template(
        "analytics/user_report.html",
        target_user=target_user,
        overview=overview,
        labs_completed=labs_completed,
        games_played=games_played,
        badges=badges,
        metrics=performance_metrics,
    )


@analytics_bp.route("/export.csv")
@login_required
def export_csv():
    """A learner may always download their own data."""
    csv_text = analytics.learner_csv(current_user)
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="cyberquest-{current_user.username}.csv"'
        },
    )


@analytics_bp.route("/cohort")
@instructor_required
def cohort():
    """Aggregate, non-identifying platform statistics for instructors."""
    return render_template(
        "analytics/cohort.html",
        overview=analytics.admin_overview(),
        hardest=analytics.hardest_labs(),
    )
