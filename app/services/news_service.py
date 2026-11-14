"""Cyber News Management & Live Feed Ingestion Service.

Enforces:
1. Curated landmark cyber attacks from the past ~1.5 years across corporate,
   healthcare, supply chain, and critical infrastructure sectors.
2. Multi-domain educational structure (Technical Anatomy, Behavioral Psychology,
   Corporate Impact, and Actionable Human Firewall Defense Checklists).
3. 1.5-Year Window Enforcement: Automatically prunes stories older than 548 days (1.5 years).
4. Live API & RSS Ingestion MVP for continuously updated real-time threat intelligence.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime, timedelta

from flask import current_app

from app.extensions import db
from app.models import CyberNews, NewsSource
from app.models.user import utcnow
from app.services.catalog_cyber_news import CURATED_CYBER_ATTACKS
from app.services.news_ingest import DEFAULT_SOURCES, _clean, ensure_default_sources

logger = logging.getLogger(__name__)

RETENTION_DAYS = 548  # Exactly 1.5 years (18 months)


def _content_hash(title: str, url: str) -> str:
    normalized = re.sub(r"\s+", " ", (title or "").strip().lower())
    return hashlib.sha256(f"{normalized}|{(url or '').strip()}".encode()).hexdigest()


def ensure_cyber_news() -> dict[str, int]:
    """Seed or update the curated 1.5-year landmark cyber attack catalog."""
    ensure_default_sources()
    default_source = NewsSource.query.filter_by(name="CISA News").first() or NewsSource.query.first()

    created = 0
    updated = 0

    for item in CURATED_CYBER_ATTACKS:
        digest = _content_hash(item["title"], item["url"])
        existing = CyberNews.query.filter_by(content_hash=digest).first()

        meta_json = json.dumps(item.get("meta", {}))

        if existing is None:
            story = CyberNews(
                source_id=default_source.id if default_source else None,
                title=item["title"],
                url=item["url"],
                content_hash=digest,
                published_at=item["published_at"],
                fetched_at=utcnow(),
                summary_en=item["summary_en"],
                summary_hi=item.get("summary_hi", ""),
                what_happened_en=item["what_happened_en"],
                what_happened_hi=item.get("what_happened_hi", ""),
                who_is_affected_en=item["who_is_affected_en"],
                who_is_affected_hi=item.get("who_is_affected_hi", ""),
                why_it_matters_en=item["why_it_matters_en"],
                why_it_matters_hi=item.get("why_it_matters_hi", ""),
                what_to_do_en=item["what_to_do_en"],
                what_to_do_hi=item.get("what_to_do_hi", ""),
                prevention_checklist_json=meta_json,
                review_state="approved",
                is_breaking=item.get("severity") == "Critical",
            )
            db.session.add(story)
            created += 1
        else:
            # Update content and ensure approved
            existing.summary_en = item["summary_en"]
            existing.summary_hi = item.get("summary_hi", "")
            existing.what_happened_en = item["what_happened_en"]
            existing.what_happened_hi = item.get("what_happened_hi", "")
            existing.who_is_affected_en = item["who_is_affected_en"]
            existing.who_is_affected_hi = item.get("who_is_affected_hi", "")
            existing.why_it_matters_en = item["why_it_matters_en"]
            existing.why_it_matters_hi = item.get("why_it_matters_hi", "")
            existing.what_to_do_en = item["what_to_do_en"]
            existing.what_to_do_hi = item.get("what_to_do_hi", "")
            existing.prevention_checklist_json = meta_json
            existing.review_state = "approved"
            existing.is_breaking = item.get("severity") == "Critical"
            updated += 1

    db.session.commit()
    prune_expired_news(max_age_days=RETENTION_DAYS)
    return {"created": created, "updated": updated, "total_curated": len(CURATED_CYBER_ATTACKS)}


def prune_expired_news(max_age_days: int = RETENTION_DAYS) -> int:
    """Enforce the 1.5-year retention rule: delete stories older than max_age_days."""
    cutoff_date = utcnow() - timedelta(days=max_age_days)
    expired_stories = CyberNews.query.filter(
        CyberNews.published_at.isnot(None),
        CyberNews.published_at < cutoff_date,
    ).all()

    deleted_count = len(expired_stories)
    for story in expired_stories:
        db.session.delete(story)

    if deleted_count > 0:
        db.session.commit()
        logger.info("Pruned %d news stories older than %d days (1.5 years)", deleted_count, max_age_days)

    return deleted_count


def get_news_feed(
    category: str | None = None,
    search: str | None = None,
    severity: str | None = None,
    limit: int = 50,
    offset: int = 0,
    include_pending: bool = False,
) -> tuple[list[CyberNews], int]:
    """Retrieve news stories with filtering, full-text search, and pagination."""
    query = CyberNews.query
    if not include_pending:
        query = query.filter_by(review_state="approved")

    if search:
        search_pattern = f"%{search.strip().lower()}%"
        query = query.filter(
            db.or_(
                CyberNews.title.ilike(search_pattern),
                CyberNews.summary_en.ilike(search_pattern),
                CyberNews.what_happened_en.ilike(search_pattern),
                CyberNews.who_is_affected_en.ilike(search_pattern),
            )
        )

    stories = query.order_by(
        CyberNews.published_at.desc().nullslast(),
        CyberNews.fetched_at.desc(),
    ).all()

    # Filter in-memory by category or severity from metadata if requested
    filtered = []
    for s in stories:
        if category and category.lower() != "all":
            if s.category.lower() != category.lower():
                continue
        if severity:
            if s.severity.lower() != severity.lower():
                continue
        filtered.append(s)

    total_count = len(filtered)
    paginated = filtered[offset : offset + limit]
    return paginated, total_count


def auto_categorize_text(text: str) -> str:
    """Intelligently assign a category based on threat intelligence keywords."""
    lowered = (text or "").lower()
    if any(k in lowered for k in ["ransomware", "encrypt", "blackcat", "alphv", "lockbit", "qilin", "blacksuit", "ransom"]):
        return "Ransomware"
    if any(k in lowered for k in ["phishing", "vishing", "social engineering", "tailgating", "impersonation", "pretext", "deepfake"]):
        return "Social Engineering"
    if any(k in lowered for k in ["cloud", "snowflake", "aws", "azure", "mfa", "token", "sso", "identity", "credential"]):
        return "Cloud & Identity"
    if any(k in lowered for k in ["supply chain", "kernel", "update", "vendor", "cve", "zero-day", "moveit", "dependency"]):
        return "Supply Chain"
    if any(k in lowered for k in ["telecom", "infrastructure", "router", "energy", "hospital", "grid", "pipeline", "scada"]):
        return "Critical Infrastructure"
    return "Corporate & Financial"


def sync_live_feeds(max_items_per_source: int = 10, auto_approve: bool = True) -> dict:
    """Fetch live feeds from authorized sources, deduplicate, auto-tag, and prune."""
    import feedparser

    ensure_default_sources()
    stats = {
        "fetched": 0,
        "new": 0,
        "skipped": 0,
        "pruned": 0,
        "errors": [],
        "timestamp": utcnow().isoformat(),
    }

    sources = NewsSource.query.filter_by(is_active=True).all()
    for src in sources:
        try:
            feed = feedparser.parse(src.feed_url)
            entries = getattr(feed, "entries", []) or []
            stats["fetched"] += len(entries)

            for entry in entries[:max_items_per_source]:
                title = _clean(getattr(entry, "title", ""))
                url = getattr(entry, "link", "") or ""
                if not title or not url:
                    continue

                digest = _content_hash(title, url)
                if CyberNews.query.filter_by(content_hash=digest).first() is not None:
                    stats["skipped"] += 1
                    continue

                published = None
                parsed = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
                if parsed:
                    try:
                        published = datetime(*parsed[:6])
                    except (TypeError, ValueError):
                        published = None

                raw_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
                cleaned_summary = _clean(raw_summary)

                category = auto_categorize_text(f"{title} {cleaned_summary}")
                meta_json = json.dumps({
                    "category": category,
                    "severity": "High" if "ransomware" in category.lower() else "Medium",
                    "technical_analysis": {"attack_vector": "Live Threat Intelligence Ingestion"},
                    "behavioral_analysis": {"human_factor": "Threat Awareness & Early Warning"},
                    "key_takeaways": [
                        "Review security configurations against incoming threat advisories.",
                        "Verify and patch exposed software versions referenced in the alert.",
                        "Reinforce employee vigilance for emerging attack campaigns."
                    ]
                })

                story = CyberNews(
                    source_id=src.id,
                    title=title[:400],
                    url=url[:700],
                    content_hash=digest,
                    published_at=published or utcnow(),
                    fetched_at=utcnow(),
                    summary_en=cleaned_summary[:1200],
                    what_happened_en=cleaned_summary[:1200],
                    prevention_checklist_json=meta_json,
                    review_state="approved" if auto_approve else "pending",
                    is_breaking=False,
                )
                db.session.add(story)
                stats["new"] += 1

            src.last_checked_at = utcnow()
            src.last_status = f"ok: {stats['new']} new added"
        except Exception as exc:
            logger.warning("Failed live sync for %s: %s", src.name, exc)
            stats["errors"].append(f"{src.name}: {str(exc)}")
            src.last_checked_at = utcnow()
            src.last_status = f"error: {type(exc).__name__}"

    db.session.commit()
    stats["pruned"] = prune_expired_news(max_age_days=RETENTION_DAYS)
    return stats

