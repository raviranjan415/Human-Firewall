"""Cyber news & live threat intelligence pages."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.extensions import db
from app.models import CyberNews, NewsSource
from app.services.news_ingest import last_checked
from app.services.news_service import get_news_feed, sync_live_feeds

news_bp = Blueprint("news", __name__)

NEWS_CATEGORIES = [
    "All",
    "Ransomware",
    "Supply Chain",
    "Cloud & Identity",
    "Social Engineering",
    "Critical Infrastructure",
    "Corporate & Financial",
]


@news_bp.route("/")
@login_required
def index():
    category = request.args.get("category", "All")
    search = request.args.get("q", "").strip()

    stories, total_count = get_news_feed(
        category=None if category == "All" else category,
        search=search if search else None,
        limit=50,
    )

    breaking_stories = (
        CyberNews.query.filter_by(review_state="approved", is_breaking=True)
        .order_by(CyberNews.published_at.desc())
        .limit(3)
        .all()
    )

    return render_template(
        "news/index.html",
        stories=stories,
        total_count=total_count,
        categories=NEWS_CATEGORIES,
        selected_category=category,
        search_query=search,
        breaking_stories=breaking_stories,
        last_checked=last_checked(),
        pending_count=CyberNews.query.filter_by(review_state="pending").count(),
    )


@news_bp.route("/sync", methods=["POST"])
@login_required
def sync():
    stats = sync_live_feeds(max_items_per_source=15, auto_approve=True)
    flash(
        f"Live Threat Feeds Synced: {stats['new']} new stories ingested, {stats['pruned']} expired stories pruned (1.5-year limit).",
        "success",
    )
    return redirect(url_for("news.index"))


@news_bp.route("/<int:news_id>")
@login_required
def detail(news_id: int):
    story = CyberNews.query.filter_by(
        id=news_id, review_state="approved"
    ).first_or_404()
    related = (
        CyberNews.query.filter(
            CyberNews.id != story.id, CyberNews.review_state == "approved"
        )
        .order_by(CyberNews.published_at.desc().nullslast())
        .limit(4)
        .all()
    )
    return render_template("news/detail.html", story=story, related=related)


@news_bp.route("/sources")
@login_required
def sources():
    return render_template(
        "news/sources.html",
        sources=NewsSource.query.order_by(NewsSource.name).all(),
        total_stories=db.session.query(CyberNews)
        .filter_by(review_state="approved")
        .count(),
    )

