"""Comprehensive tests for Cyber News Today: Live Threat Intelligence, 1.5-Year Retention, Multi-Domain Analysis, and REST APIs."""

from __future__ import annotations

from datetime import timedelta
import pytest

from app.models import CyberNews, NewsSource
from app.models.user import utcnow
from app.services.catalog_cyber_news import CURATED_CYBER_ATTACKS
from app.services.news_service import (
    ensure_cyber_news,
    get_news_feed,
    prune_expired_news,
)
from .conftest import LEARNER_PASSWORD, login


def test_curated_attacks_catalog_integrity():
    """Verify landmark cyber attacks have required multi-domain fields."""
    assert len(CURATED_CYBER_ATTACKS) >= 12
    for attack in CURATED_CYBER_ATTACKS:
        assert attack.get("title")
        assert attack.get("category")
        assert attack.get("severity") in ("Critical", "High", "Medium")
        assert attack.get("financial_impact")
        assert attack.get("summary_en")
        assert attack.get("what_happened_en")
        assert attack.get("who_is_affected_en")
        assert attack.get("why_it_matters_en")
        assert attack.get("what_to_do_en")
        meta = attack.get("meta", {})
        assert "technical_analysis" in meta
        assert "behavioral_analysis" in meta
        assert "key_takeaways" in meta


def test_18_month_retention_prunes_old_stories(app, db):
    """Verify strict 1.5-year (548 days) retention window auto-prunes older items."""
    now = utcnow()

    # Story 1: Within retention window (30 days old)
    recent_story = CyberNews(
        title="Recent Attack within 1.5 Years",
        url="https://example.com/recent-1",
        content_hash="recent1" * 8,
        published_at=now - timedelta(days=30),
        review_state="approved",
    )

    # Story 2: Exactly 540 days old (still within 548 days)
    border_story = CyberNews(
        title="Borderline Attack (540 days old)",
        url="https://example.com/border-1",
        content_hash="border1" * 8,
        published_at=now - timedelta(days=540),
        review_state="approved",
    )

    # Story 3: Beyond retention window (600 days old)
    expired_story = CyberNews(
        title="Old Attack from 2024 (600 days old)",
        url="https://example.com/expired-1",
        content_hash="expired1" * 8,
        published_at=now - timedelta(days=600),
        review_state="approved",
    )

    db.session.add_all([recent_story, border_story, expired_story])
    db.session.commit()

    # Run pruning
    pruned_count = prune_expired_news(max_age_days=548)
    assert pruned_count >= 1

    # Recent and border story should survive; expired story must be deleted
    assert CyberNews.query.filter_by(content_hash="recent1" * 8).first() is not None
    assert CyberNews.query.filter_by(content_hash="border1" * 8).first() is not None
    assert CyberNews.query.filter_by(content_hash="expired1" * 8).first() is None


def test_ensure_cyber_news_seeds_properly(app, db):
    """Verify ensure_cyber_news populates landmark approved attacks."""
    stats = ensure_cyber_news()
    assert stats["created"] + stats["updated"] >= 12
    approved = CyberNews.query.filter_by(review_state="approved").count()
    assert approved >= 12


def test_api_news_feed_endpoints(client, app, db):
    """Test REST API /api/news/feed and filtering."""
    ensure_cyber_news()

    # 1. Default feed
    res = client.get("/api/news/feed")
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert data["retention_policy_days"] == 548
    assert data["retention_window"] == "1.5 years (548 days)"
    assert len(data["stories"]) > 0

    # 2. Filter by category
    res_cat = client.get("/api/news/feed?category=Ransomware")
    assert res_cat.status_code == 200
    cat_data = res_cat.get_json()
    assert cat_data["ok"] is True
    for item in cat_data["stories"]:
        assert "Ransomware" in item["category"] or "ransomware" in item["title"].lower()

    # 3. Filter by search
    res_search = client.get("/api/news/feed?search=CrowdStrike")
    assert res_search.status_code == 200
    search_data = res_search.get_json()
    assert search_data["ok"] is True
    assert any("CrowdStrike" in item["title"] for item in search_data["stories"])

    # 4. Filter by severity
    res_sev = client.get("/api/news/feed?severity=Critical")
    assert res_sev.status_code == 200
    sev_data = res_sev.get_json()
    assert sev_data["ok"] is True
    for item in sev_data["stories"]:
        assert item["severity"] == "Critical"


def test_api_news_detail_and_multi_domain_structure(client, app, db):
    """Test REST API /api/news/<id> returning full multi-domain schema."""
    ensure_cyber_news()
    story = CyberNews.query.filter_by(review_state="approved").first()
    assert story is not None

    res = client.get(f"/api/news/{story.id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    s = data["story"]
    assert s["id"] == story.id
    assert s["title"] == story.title
    assert "technical_analysis" in s
    assert "behavioral_analysis" in s
    assert "financial_impact" in s
    assert "what_to_do" in s


def test_cyber_news_web_ui(client, learner, app, db):
    """Test Web UI routes /cyber-news/ and /cyber-news/<id>."""
    ensure_cyber_news()
    login(client, "learner1")

    # 1. Main index page
    res = client.get("/cyber-news/")
    assert res.status_code == 200
    assert b"Cyber News Today" in res.data
    assert b"548-Day" in res.data
    assert b"Sync Live Feeds" in res.data
    assert b"REST API Feed" in res.data

    # 2. Category filtering on Web UI
    res_cat = client.get("/cyber-news/?category=Ransomware")
    assert res_cat.status_code == 200

    # 3. Search on Web UI
    res_search = client.get("/cyber-news/?q=CrowdStrike")
    assert res_search.status_code == 200
    assert b"CrowdStrike" in res.data

    # 4. Detail page on Web UI
    story = CyberNews.query.filter_by(review_state="approved").first()
    res_detail = client.get(f"/cyber-news/{story.id}")
    assert res_detail.status_code == 200
    assert story.title.encode("utf-8") in res_detail.data
    assert b"Technical Anatomy" in res_detail.data
    assert b"Behavioral &amp; Human Factors" in res_detail.data or b"Behavioral & Human Factors" in res_detail.data
    assert b"Human Firewall Action" in res_detail.data
