"""Historical incident library ("What Happened?").

Every case carries a confidence label and a source list so confirmed facts are
never presented as though they were verified reporting, or the reverse.
"""

from __future__ import annotations

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.extensions import db
from app.models import HistoricalIncident

incidents_bp = Blueprint("incidents", __name__)

CONFIDENCE_ORDER = ("confirmed", "reported", "interpretation", "disputed")


@incidents_bp.route("/")
@login_required
def index():
    search = (request.args.get("q") or "").strip()
    sector = (request.args.get("sector") or "").strip()
    category = (request.args.get("category") or "").strip()
    confidence = (request.args.get("confidence") or "").strip()

    query = HistoricalIncident.query.filter_by(state="published")
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                HistoricalIncident.title_en.ilike(like),
                HistoricalIncident.organization.ilike(like),
                HistoricalIncident.summary_en.ilike(like),
            )
        )
    if sector:
        query = query.filter(HistoricalIncident.sector == sector)
    if category:
        query = query.filter(HistoricalIncident.category == category)
    if confidence:
        query = query.filter(HistoricalIncident.confidence == confidence)

    def _distinct(column):
        return [
            row[0]
            for row in db.session.query(column)
            .filter(HistoricalIncident.state == "published", column.isnot(None))
            .distinct()
            .order_by(column)
            .all()
        ]

    return render_template(
        "incidents/index.html",
        incidents=query.order_by(HistoricalIncident.year.desc()).all(),
        sectors=_distinct(HistoricalIncident.sector),
        categories=_distinct(HistoricalIncident.category),
        confidence_levels=CONFIDENCE_ORDER,
        selected={"q": search, "sector": sector, "category": category, "confidence": confidence},
    )


@incidents_bp.route("/<slug>")
@login_required
def detail(slug: str):
    incident = HistoricalIncident.query.filter_by(slug=slug, state="published").first_or_404()
    return render_template("incidents/detail.html", incident=incident)
