"""Incident intelligence, news ingestion and community models."""

from app.extensions import db
from app.models.user import TimestampMixin, utcnow

# How confident the platform is about the documented facts.
CONFIDENCE_LEVELS = ("confirmed", "reported", "interpretation", "disputed")


class HistoricalIncident(db.Model, TimestampMixin):
    """A researched real-world cyber incident ("What Happened?")."""

    __tablename__ = "historical_incidents"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    title_en = db.Column(db.String(240), nullable=False)
    title_hi = db.Column(db.String(240))
    year = db.Column(db.Integer, nullable=False, index=True)
    organization = db.Column(db.String(240))
    sector = db.Column(db.String(120), index=True)
    category = db.Column(db.String(120), index=True)
    attack_type = db.Column(db.String(120))
    human_factor = db.Column(db.Boolean, default=True, nullable=False)

    summary_en = db.Column(db.Text)
    summary_hi = db.Column(db.Text)
    what_happened_en = db.Column(db.Text)
    what_happened_hi = db.Column(db.Text)
    how_it_worked_en = db.Column(db.Text)
    how_it_worked_hi = db.Column(db.Text)
    weaknesses_en = db.Column(db.Text)
    weaknesses_hi = db.Column(db.Text)
    consequences_en = db.Column(db.Text)
    consequences_hi = db.Column(db.Text)
    discovery_en = db.Column(db.Text)
    discovery_hi = db.Column(db.Text)
    response_en = db.Column(db.Text)
    response_hi = db.Column(db.Text)
    remediation_en = db.Column(db.Text)
    remediation_hi = db.Column(db.Text)
    precautions_en = db.Column(db.Text)
    precautions_hi = db.Column(db.Text)
    lessons_en = db.Column(db.Text)      # JSON list of 5 lesson strings
    lessons_hi = db.Column(db.Text)
    technical_detail_en = db.Column(db.Text)   # expandable "advanced" section
    technical_detail_hi = db.Column(db.Text)

    confidence = db.Column(db.String(24), default="confirmed", nullable=False)
    uncertainty_note_en = db.Column(db.Text)
    uncertainty_note_hi = db.Column(db.Text)
    source_published_on = db.Column(db.Date)
    last_reviewed_on = db.Column(db.Date)
    state = db.Column(db.String(24), default="published", nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)

    sources = db.relationship(
        "IncidentSource", back_populates="incident", cascade="all, delete-orphan"
    )


class IncidentSource(db.Model):
    __tablename__ = "incident_sources"

    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(
        db.Integer, db.ForeignKey("historical_incidents.id", ondelete="CASCADE"), nullable=False
    )
    label = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(600), nullable=False)
    publisher = db.Column(db.String(160))
    published_on = db.Column(db.Date)

    incident = db.relationship("HistoricalIncident", back_populates="sources")


class NewsSource(db.Model, TimestampMixin):
    __tablename__ = "news_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), unique=True, nullable=False)
    feed_url = db.Column(db.String(600), nullable=False)
    homepage = db.Column(db.String(300))
    # Only RSS / authorized APIs — never scrape against a site's terms.
    kind = db.Column(db.String(24), default="rss", nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_checked_at = db.Column(db.DateTime)
    last_status = db.Column(db.String(120))
    rate_limit_seconds = db.Column(db.Integer, default=900, nullable=False)


class CyberNews(db.Model, TimestampMixin):
    __tablename__ = "cyber_news"

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("news_sources.id", ondelete="SET NULL"))
    title = db.Column(db.String(400), nullable=False)
    url = db.Column(db.String(700), nullable=False)
    content_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    published_at = db.Column(db.DateTime, index=True)
    fetched_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    summary_en = db.Column(db.Text)
    summary_hi = db.Column(db.Text)
    what_happened_en = db.Column(db.Text)
    what_happened_hi = db.Column(db.Text)
    who_is_affected_en = db.Column(db.Text)
    who_is_affected_hi = db.Column(db.Text)
    why_it_matters_en = db.Column(db.Text)
    why_it_matters_hi = db.Column(db.Text)
    what_to_do_en = db.Column(db.Text)
    what_to_do_hi = db.Column(db.Text)
    prevention_checklist_json = db.Column(db.Text)
    related_lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"))
    related_lab_id = db.Column(db.Integer, db.ForeignKey("labs.id"))

    # review_state: pending | approved | rejected
    review_state = db.Column(db.String(24), default="pending", nullable=False, index=True)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_breaking = db.Column(db.Boolean, default=False, nullable=False)

    source = db.relationship("NewsSource")


class CommunityPost(db.Model, TimestampMixin):
    __tablename__ = "community_posts"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    group_name = db.Column(db.String(120))
    topic = db.Column(db.String(160), index=True)
    body = db.Column(db.Text, nullable=False)
    is_hidden = db.Column(db.Boolean, default=False, nullable=False)
    report_count = db.Column(db.Integer, default=0, nullable=False)


class ModerationReport(db.Model):
    __tablename__ = "moderation_reports"

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    post_id = db.Column(db.Integer, db.ForeignKey("community_posts.id", ondelete="CASCADE"))
    reason = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(24), default="open", nullable=False, index=True)
    handled_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
