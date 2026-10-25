"""Cyber news pages.

Only stories an administrator has approved are visible to learners. Nothing is
shown as breaking news unless it genuinely is.
"""

from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import login_required

from app.extensions import db
from app.models import CyberNews, NewsSource
from app.services.news_ingest import approved_news, last_checked

news_bp = Blueprint("news", __name__)


@news_bp.route("/")
@login_required
def index():
    return render_template(
        "news/index.html",
        stories=approved_news(limit=40),
        last_checked=last_checked(),
        pending_count=CyberNews.query.filter_by(review_state="pending").count(),
    )


@news_bp.route("/<int:news_id>")
@login_required
def detail(news_id: int):
    story = CyberNews.query.filter_by(id=news_id, review_state="approved").first_or_404()
    related = (
        CyberNews.query.filter(
            CyberNews.id != story.id, CyberNews.review_state == "approved"
        )
        .order_by(CyberNews.published_at.desc().nullslast())
        .limit(5)
        .all()
    )
    return render_template("news/detail.html", story=story, related=related)


@news_bp.route("/sources")
@login_required
def sources():
    return render_template(
        "news/sources.html",
        sources=NewsSource.query.order_by(NewsSource.name).all(),
        total_stories=db.session.query(CyberNews).filter_by(review_state="approved").count(),
    )
