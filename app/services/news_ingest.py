"""Daily cyber-news ingestion from permitted RSS feeds and authorized APIs.

Rules enforced here (specification section 14):
  * Only RSS/API sources are fetched — never a site that forbids scraping.
  * Stories are deduplicated by content hash.
  * Publication dates and the original source are always stored.
  * Nothing is published to learners until an administrator approves it.
  * When a source is unreachable, the last verified stories keep their real
    dates — old incidents are never relabelled as breaking news.
"""

from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime, timedelta

from flask import current_app

from app.extensions import db
from app.models import CyberNews, NewsSource
from app.models.user import utcnow

logger = logging.getLogger(__name__)

DEFAULT_SOURCES = [
    {
        "name": "CISA News",
        "feed_url": "https://www.cisa.gov/news.xml",
        "homepage": "https://www.cisa.gov/news-events/news",
        "kind": "rss",
    },
    {
        "name": "CISA Cybersecurity Advisories",
        "feed_url": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
        "homepage": "https://www.cisa.gov/news-events/cybersecurity-advisories",
        "kind": "rss",
    },
    {
        "name": "Krebs on Security",
        "feed_url": "https://krebsonsecurity.com/feed/",
        "homepage": "https://krebsonsecurity.com/",
        "kind": "rss",
    },
    {
        "name": "The Hacker News",
        "feed_url": "https://feeds.feedburner.com/TheHackersNews",
        "homepage": "https://thehackernews.com/",
        "kind": "rss",
    },
    {
        "name": "BleepingComputer",
        "feed_url": "https://www.bleepingcomputer.com/feed/",
        "homepage": "https://www.bleepingcomputer.com/",
        "kind": "rss",
    },
]


def ensure_default_sources() -> int:
    """Register the built-in sources once. Returns how many were created."""
    created = 0
    for source in DEFAULT_SOURCES:
        if NewsSource.query.filter_by(name=source["name"]).first() is None:
            db.session.add(NewsSource(**source))
            created += 1
    if created:
        db.session.commit()
    return created


def _content_hash(title: str, url: str) -> str:
    normalized = re.sub(r"\s+", " ", (title or "").strip().lower())
    return hashlib.sha256(f"{normalized}|{(url or '').strip()}".encode("utf-8")).hexdigest()


def _clean(html: str | None) -> str:
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _structure_summary(summary: str, source_name: str) -> dict:
    """Build the platform's article skeleton from the original summary.

    The factual fields stay empty until an administrator (or a reviewer
    verifying against the original source) fills them in, so nothing is
    invented on the learner's behalf.
    """
    summary = (summary or "")[:1200]
    return {
        "summary_en": summary,
        "summary_hi": "",
        "what_happened_en": summary,
        "what_happened_hi": "",
        "who_is_affected_en": "",
        "why_it_matters_en": "",
        "what_to_do_en": "",
        "prevention_checklist_json": None,
    }


def ingest_source(source: NewsSource, max_items: int | None = None) -> dict:
    """Fetch one source and store new, deduplicated stories."""
    import feedparser

    max_items = max_items or current_app.config.get("NEWS_MAX_ITEMS_PER_SOURCE", 15)
    result = {"source": source.name, "fetched": 0, "new": 0, "skipped": 0, "error": None}

    if source.rate_limit_seconds:
        last = source.last_checked_at
        if last and utcnow() - last < timedelta(seconds=source.rate_limit_seconds):
            result["error"] = "rate_limited_locally"
            return result

    try:
        feed = feedparser.parse(source.feed_url)
        entries = getattr(feed, "entries", []) or []
        result["fetched"] = len(entries)
    except Exception as exc:  # network failures must never crash the app
        logger.warning("News source %s failed: %s", source.name, exc)
        source.last_checked_at = utcnow()
        source.last_status = f"error: {type(exc).__name__}"
        db.session.commit()
        result["error"] = "fetch_failed"
        return result

    if getattr(feed, "bozo", 0) and not entries:
        source.last_checked_at = utcnow()
        source.last_status = "error: unreadable feed"
        db.session.commit()
        result["error"] = "unreadable_feed"
        return result

    for entry in entries[:max_items]:
        title = _clean(getattr(entry, "title", ""))
        url = getattr(entry, "link", "") or ""
        if not title or not url:
            continue
        digest = _content_hash(title, url)
        if CyberNews.query.filter_by(content_hash=digest).first() is not None:
            result["skipped"] += 1
            continue

        published = None
        parsed = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
        if parsed:
            try:
                published = datetime(*parsed[:6])
            except (TypeError, ValueError):
                published = None

        raw_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
        structured = _structure_summary(_clean(raw_summary), source.name)

        db.session.add(
            CyberNews(
                source_id=source.id,
                title=title[:400],
                url=url[:700],
                content_hash=digest,
                published_at=published,
                review_state="pending",
                is_breaking=False,
                **structured,
            )
        )
        result["new"] += 1

    source.last_checked_at = utcnow()
    source.last_status = f"ok: {result['new']} new / {result['fetched']} seen"
    db.session.commit()
    return result


def ingest_all() -> list[str]:
    """Fetch every active source. Returns human-readable log lines."""
    ensure_default_sources()
    lines = []
    max_items = current_app.config.get("NEWS_MAX_ITEMS_PER_SOURCE", 15)
    for source in NewsSource.query.filter_by(is_active=True).all():
        result = ingest_source(source, max_items)
        if result["error"]:
            lines.append(f"{source.name}: {result['error']} (no stories imported)")
        else:
            lines.append(
                f"{source.name}: {result['new']} new, {result['skipped']} duplicates skipped"
            )
    return lines


def approved_news(limit: int = 30, include_pending: bool = False) -> list[CyberNews]:
    query = CyberNews.query
    if not include_pending:
        query = query.filter_by(review_state="approved")
    return query.order_by(CyberNews.published_at.desc().nullslast(), CyberNews.fetched_at.desc()).limit(limit).all()


def last_checked() -> datetime | None:
    return (
        db.session.query(db.func.max(NewsSource.last_checked_at)).scalar()
    )
