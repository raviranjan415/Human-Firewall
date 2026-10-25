"""Analytics pages: a learner's own data, a cohort view for instructors and CSV export."""

from __future__ import annotations

from flask import Blueprint, Response, render_template
from flask_login import current_user, login_required

from app.auth.decorators import instructor_required
from app.services import analytics

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/")
@login_required
def index():
    """Everything reported here is measured from this learner's own activity."""
    return render_template("analytics/index.html", overview=analytics.learner_overview(current_user))


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
