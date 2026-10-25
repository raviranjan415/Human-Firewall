"""News ingestion rules (RSS only, deduplicated, human-reviewed) and seeding."""

from __future__ import annotations

import feedparser

from app.models import (
    Achievement,
    Comic,
    CyberNews,
    Game,
    HistoricalIncident,
    Lab,
    LearningPath,
    Lesson,
    NewsSource,
    Role,
    User,
    VideoAsset,
)
from app.services import news_ingest
from app.services.news_ingest import _content_hash
from app.services.seed import run_seed

from .conftest import ADMIN_USERNAME, login


class _Entry:
    def __init__(self, title, link, summary=""):
        self.title = title
        self.link = link
        self.summary = summary


class _Feed:
    def __init__(self, entries):
        self.entries = entries
        self.bozo = 0


def test_content_hash_is_stable_and_case_insensitive():
    a = _content_hash("Breaking  News", "https://example.com/a")
    b = _content_hash("breaking news", "https://example.com/a")
    c = _content_hash("Breaking News", "https://example.com/b")
    assert a == b
    assert a != c


def test_default_sources_are_rss_only(app):
    sources = NewsSource.query.all()
    assert sources
    for source in sources:
        assert source.kind == "rss"
        assert source.feed_url.startswith("https://")


def test_ingestion_deduplicates_and_never_publishes_directly(app, monkeypatch, db):
    source = NewsSource.query.first()
    monkeypatch.setattr(
        feedparser,
        "parse",
        lambda url: _Feed([_Entry("Story one", "https://example.com/one", "Details here")]),
    )
    source.rate_limit_seconds = 0
    source.last_checked_at = None
    db.session.commit()

    first = news_ingest.ingest_source(source)
    assert first["new"] == 1
    assert first["skipped"] == 0

    second = news_ingest.ingest_source(source)
    assert second["new"] == 0
    assert second["skipped"] == 1

    assert CyberNews.query.filter_by(url="https://example.com/one").count() == 1
    # Nothing reaches learners until an administrator approves it.
    assert CyberNews.query.first().review_state == "pending"
    assert news_ingest.approved_news() == []


def test_unreachable_source_is_recorded_without_crashing(app, monkeypatch, db):
    source = NewsSource.query.first()
    source.rate_limit_seconds = 0
    source.last_checked_at = None
    db.session.commit()

    def _boom(url):
        raise OSError("network down")

    monkeypatch.setattr(feedparser, "parse", _boom)
    result = news_ingest.ingest_source(source)
    assert result["error"] == "fetch_failed"
    assert result["new"] == 0
    assert source.last_status.startswith("error:")


def test_local_rate_limit_defers_repeated_fetches(app, monkeypatch, db):
    source = NewsSource.query.first()
    source.rate_limit_seconds = 900
    db.session.commit()

    news_ingest.ingest_source(source)
    again = news_ingest.ingest_source(source)
    assert again["error"] == "rate_limited_locally"

    source.rate_limit_seconds = 0
    db.session.commit()


def test_approved_news_only_returns_approved_stories(app, db):
    db.session.add_all(
        [
            CyberNews(title="Approved", url="https://example.com/a1",
                      content_hash="1" * 64, review_state="approved"),
            CyberNews(title="Pending", url="https://example.com/a2",
                      content_hash="2" * 64, review_state="pending"),
            CyberNews(title="Rejected", url="https://example.com/a3",
                      content_hash="3" * 64, review_state="rejected"),
        ]
    )
    db.session.commit()

    titles = [story.title for story in news_ingest.approved_news()]
    assert titles == ["Approved"]


def test_news_page_lists_approved_stories(client, learner, db):
    db.session.add(
        CyberNews(title="Verified advisory", url="https://example.com/v1",
                  content_hash="4" * 64, review_state="approved",
                  what_happened_en="Something happened.")
    )
    db.session.commit()

    login(client, "learner1")
    response = client.get("/cyber-news/")
    assert response.status_code == 200
    assert b"Verified advisory" in response.data


def test_news_sources_page_lists_the_configured_feeds(client, learner):
    login(client, "learner1")
    response = client.get("/cyber-news/sources")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Seeding
# ---------------------------------------------------------------------------

def test_roles_are_seeded(app):
    names = {role.name for role in Role.query.all()}
    assert names == {"learner", "instructor", "admin", "org_admin"}


def test_seed_is_idempotent(app):
    before = (
        Role.query.count(),
        Achievement.query.count(),
        Lab.query.count(),
        Game.query.count(),
        Lesson.query.count(),
        VideoAsset.query.count(),
        Comic.query.count(),
        HistoricalIncident.query.count(),
        NewsSource.query.count(),
    )
    run_seed(with_demo=False)
    after = (
        Role.query.count(),
        Achievement.query.count(),
        Lab.query.count(),
        Game.query.count(),
        Lesson.query.count(),
        VideoAsset.query.count(),
        Comic.query.count(),
        HistoricalIncident.query.count(),
        NewsSource.query.count(),
    )
    assert before == after


def test_catalogue_matches_the_seeded_content(app):
    assert Lab.query.count() == 100
    assert Lab.query.filter_by(state="published").count() == 40
    assert Lab.query.filter_by(state="draft").count() == 60
    assert LearningPath.query.count() >= 1
    assert Lesson.query.count() >= 1
    assert Comic.query.count() >= 1
    assert Game.query.count() >= 1
    assert HistoricalIncident.query.count() >= 1
    assert Achievement.query.count() == 17


def test_prototype_media_is_flagged_honestly(app):
    videos = VideoAsset.query.all()
    assert videos
    for video in videos:
        assert video.is_prototype is True
        assert video.script_en


def test_lab_prerequisites_form_an_ordered_chain(app):
    second = Lab.query.filter_by(number=2).first()
    first = Lab.query.filter_by(number=1).first()
    assert [p.requires_lab_id for p in second.prerequisites] == [first.id]


def test_historical_incidents_carry_a_confidence_label(app):
    labels = {incident.confidence for incident in HistoricalIncident.query.all()}
    assert labels
    for incident in HistoricalIncident.query.all():
        assert incident.confidence in (
            "confirmed", "reported", "interpretation", "disputed"
        )
        assert incident.last_reviewed_on is not None


def test_bootstrap_admin_account_exists(app):
    admin = User.query.filter_by(username=ADMIN_USERNAME).first()
    assert admin is not None
    assert admin.is_admin is True
    assert admin.email_verified is True
