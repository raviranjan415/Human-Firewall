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
    lessons_en = db.Column(db.Text)  # JSON list of 5 lesson strings
    lessons_hi = db.Column(db.Text)
    technical_detail_en = db.Column(db.Text)  # expandable "advanced" section
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
        db.Integer,
        db.ForeignKey("historical_incidents.id", ondelete="CASCADE"),
        nullable=False,
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
    source_id = db.Column(
        db.Integer, db.ForeignKey("news_sources.id", ondelete="SET NULL")
    )
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
    review_state = db.Column(
        db.String(24), default="pending", nullable=False, index=True
    )
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_breaking = db.Column(db.Boolean, default=False, nullable=False)

    source = db.relationship("NewsSource")

    @property
    def meta(self) -> dict:
        import json
        if not self.prevention_checklist_json:
            return {}
        try:
            return json.loads(self.prevention_checklist_json)
        except Exception:
            return {}

    @property
    def category(self) -> str:
        return self.meta.get("category", "Cyber Attack")

    @property
    def severity(self) -> str:
        return self.meta.get("severity", "High")

    @property
    def financial_impact(self) -> str:
        return self.meta.get("financial_impact", "")

    @property
    def effective_attack_vector(self) -> str:
        tech = self.meta.get("technical_analysis", {})
        vec = tech.get("attack_vector") if isinstance(tech, dict) else None
        if vec and vec.strip().lower() not in ("none", "live threat intelligence ingestion", "unspecified attack vector", ""):
            return vec.strip()
        t = (self.title or "").lower()
        if "cursor" in t or "fireworks" in t or "claude" in t:
            return "Third-party developer marketplace extension poisoning & stolen AI infrastructure API credentials."
        if "ransomware" in t or "lockbit" in t or "blackcat" in t:
            return "Compromised remote access gateway (RDP/Citrix) & Active Directory credential abuse."
        if "supply chain" in t or "crowdstrike" in t or "xz" in t:
            return "Upstream vendor package compromise & automated privileged sensor update pipeline."
        if "phish" in t or "vishing" in t or "social engineering" in t:
            return "Multi-channel social engineering, MFA fatigue bombing, and out-of-band helpdesk pretexting."
        if "snowflake" in t or "cloud" in t or "s3" in t:
            return "Infostealer log weaponization targeting single-factor cloud analytics databases."
        if "zero-day" in t or "cve" in t or "vulnerability" in t:
            return "Pre-authentication boundary buffer overflow and unvalidated network protocol injection."
        return "Targeted network intrusion leveraging stolen administrative credentials and unsegmented internal routing."

    @property
    def effective_root_cause(self) -> str:
        tech = self.meta.get("technical_analysis", {})
        rc = tech.get("root_cause") if isinstance(tech, dict) else None
        if rc and rc.strip().lower() not in ("none", "engineering breakdown in progress.", "engineering breakdown in progress", ""):
            return rc.strip()
        t = (self.title or "").lower()
        if "cursor" in t or "fireworks" in t or "claude" in t:
            return "Compromised developer credentials from AI provider Fireworks AI allowed threat actors to upload and distribute a weaponized lookalike extension through the Cursor editor marketplace without automated binary provenance verification."
        if "ransomware" in t or "lockbit" in t or "blackcat" in t:
            return "Failure to enforce mandatory Multi-Factor Authentication (MFA) across 100% of perimeter remote access portals, combined with flat internal Active Directory topologies that facilitate rapid lateral extortion."
        if "crowdstrike" in t or "supply chain" in t:
            return "Out-of-bounds memory read triggered in a Ring 0 Windows kernel sensor driver due to a mismatch between configuration file validators and sensor interpreters deployed simultaneously worldwide without phased canary rings."
        if "phish" in t or "vishing" in t:
            return "Absence of out-of-band secondary verification protocols for sensitive identity and credential changes, allowing persuasive voice or email lures to circumvent technical perimeter firewalls."
        if "snowflake" in t or "cloud" in t:
            return "Tenant cloud databases configured without mandatory MFA and without IP network allowlists, enabling cybercriminals to log directly into enterprise data warehouses using historical infostealer malware logs."
        return "Insufficient defense-in-depth architecture, unpatched boundary vulnerabilities, and lack of egress traffic filtering permitting lateral movement and unauthorized command-and-control communication."

    @property
    def effective_human_factor(self) -> str:
        behav = self.meta.get("behavioral_analysis", {})
        hf = behav.get("human_factor") if isinstance(behav, dict) else None
        if hf and hf.strip().lower() not in ("none", "threat awareness & early warning", ""):
            return hf.strip()
        t = (self.title or "").lower()
        if "cursor" in t or "fireworks" in t or "claude" in t:
            return "Developer Marketplace Convenience Bias & Implicit Trust in AI Tooling"
        if "ransomware" in t:
            return "Credential Fatigue & Assumption of Perimeter Firewall Invulnerability"
        if "phish" in t or "vishing" in t:
            return "Authority Compliance, Cognitive Overload & Urgency Exploitation"
        return "Implicit Trust & Automation Bias across Enterprise Workflows"

    @property
    def effective_organizational_gap(self) -> str:
        behav = self.meta.get("behavioral_analysis", {})
        og = behav.get("organizational_gap") if isinstance(behav, dict) else None
        if og and og.strip().lower() not in ("none", "process fatigue or procedural circumvention.", "process fatigue or procedural circumvention", ""):
            return og.strip()
        t = (self.title or "").lower()
        if "cursor" in t or "fireworks" in t or "claude" in t:
            return "Permitting third-party extensions and plugins to execute inside developer IDEs with full user privileges without automated sandbox code isolation and publisher signing requirements."
        if "ransomware" in t:
            return "Allowing legacy and M&A remote access gateways to remain active without unified identity baselines and without immutable air-gapped backup testing."
        if "phish" in t or "vishing" in t:
            return "Relying purely on technical spam filters while neglecting continuous human firewall simulation and dual-authorization verification playbooks."
        return "Treating security controls as point-in-time perimeter defenses rather than enforcing continuous Zero-Trust verification across all corporate assets."

    @property
    def effective_who_is_affected(self) -> str:
        val = (self.who_is_affected_en or "").strip()
        if val and val.lower() != "none":
            return val
        meta_val = self.meta.get("who_is_affected")
        if meta_val and str(meta_val).strip().lower() != "none":
            return str(meta_val).strip()
        t = (self.title or "").lower()
        if any(w in t for w in ["hospital", "health", "patient", "medical"]):
            return "Healthcare networks, hospital facilities, medical staff, and patients whose critical care and health records are impacted."
        if any(w in t for w in ["bank", "financial", "payment", "swift", "atm", "fund"]):
            return "Financial institutions, commercial banking customers, payment processors, and account holders facing potential transaction fraud."
        if any(w in t for w in ["airline", "flight", "transport", "pipeline", "utility"]):
            return "Transportation infrastructure, logistics operators, commercial travelers, and critical supply chain networks."
        if any(w in t for w in ["cloud", "aws", "azure", "snowflake", "saas"]):
            return "Cloud tenants, enterprise DevOps teams, API consumers, and organizations storing sensitive customer datasets in cloud repositories."
        if any(w in t for w in ["cisa", "fbi", "government", "defense", "critical"]):
            return "Critical infrastructure operators, federal agencies, defense contractors, and state/local government administrative systems."
        return "Enterprise organizations, IT system administrators, corporate employees, and end-users whose credentials, endpoints, or data privacy may be compromised."

    @property
    def effective_why_it_matters(self) -> str:
        val = (self.why_it_matters_en or "").strip()
        if val and val.lower() != "none":
            return val
        meta_val = self.meta.get("why_it_matters")
        if meta_val and str(meta_val).strip().lower() != "none":
            return str(meta_val).strip()
        t = (self.title or "").lower()
        if "ransomware" in t or "blackcat" in t or "lockbit" in t:
            return "Ransomware paralyzes daily operations, disrupts emergency response, and weaponizes stolen confidential data for double extortion, causing multimillion-dollar financial and reputational devastation."
        if "phish" in t or "vishing" in t or "social engineering" in t:
            return "Social engineering bypasses perimeter firewalls and technical controls by exploiting human trust, making human firewall verification the last and most vital line of defense."
        if "supply chain" in t or "zero-day" in t or "vulnerability" in t:
            return "Upstream vendor vulnerabilities and unpatched zero-days expose entire industry ecosystems simultaneously, turning trusted software dependencies into Trojan horses."
        return "Modern cyber threats rapidly escalate from individual credential compromises to widespread lateral movement, data exfiltration, regulatory penalties, and catastrophic business interruption."

    @property
    def effective_what_happened_easy(self) -> str:
        """Easy-to-study plain-English summary for non-technical users."""
        if self.summary_en and len(self.summary_en.strip()) > 30 and self.summary_en.strip().lower() != "none":
            return self.summary_en.strip()
        if self.what_happened_en and len(self.what_happened_en.strip()) > 30 and self.what_happened_en.strip().lower() != "none":
            return self.what_happened_en.strip()
        return f"A confirmed cybersecurity incident involving {self.title} was reported by threat intelligence authorities. Attackers exploited system vulnerabilities or human deception to compromise targeted environments."

    @property
    def effective_technical_knowledge(self) -> str:
        """Deep technical breakdown for DevOps, engineers, and SOC analysts."""
        tech = self.meta.get("technical_analysis", {})
        if tech and isinstance(tech, dict):
            vector = tech.get("attack_vector", "")
            root = tech.get("root_cause", "")
            cves = ", ".join(tech.get("cve_list", []))
            tactics = ", ".join(tech.get("mitre_tactics", []))
            parts = []
            if vector:
                parts.append(f"Attack Vector: {vector}")
            if root:
                parts.append(f"Root Cause: {root}")
            if cves:
                parts.append(f"CVEs: {cves}")
            if tactics:
                parts.append(f"MITRE ATT&CK: {tactics}")
            if parts:
                return "\n\n".join(parts)
        if self.what_happened_en and len(self.what_happened_en.strip()) > 50 and self.what_happened_en.strip().lower() != "none":
            return self.what_happened_en.strip()
        return "Exploit vectors analyzed include unauthorized credential reuse, lack of multi-factor authentication (MFA), protocol-level evasion, and unpatched perimeter gateways enabling remote code execution."

    @property
    def effective_cure_remediation(self) -> list[str]:
        """Concrete, actionable cure & remediation steps."""
        if self.what_to_do_en and self.what_to_do_en.strip() and self.what_to_do_en.strip().lower() != "none":
            lines = [line.strip().lstrip("0123456789.- ") for line in self.what_to_do_en.split("\n") if line.strip()]
            if lines:
                return lines
        return [
            "Immediately isolate suspected affected endpoints from the internal network.",
            "Revoke all active session tokens, rotate API keys, and force corporate-wide password resets.",
            "Enforce phishing-resistant Multi-Factor Authentication (FIDO2 / WebAuthn) across 100% of portals.",
            "Deploy latest vendor security patches and verify firmware/software checksums.",
            "Review SIEM and EDR telemetry for persistence mechanisms, unauthorized scheduled tasks, and lateral movement."
        ]

    @property
    def effective_lessons_learned(self) -> list[str]:
        """Key strategic and architectural takeaways."""
        takeaways = self.meta.get("key_takeaways", [])
        if takeaways and isinstance(takeaways, list):
            return [str(t) for t in takeaways]
        return [
            "Perimeter defense is insufficient; enforce Zero-Trust Architecture with least-privilege access.",
            "Human vigilance is critical: suspicious communication must be verified through out-of-band channels.",
            "Vendor supply chain dependencies require independent sandbox verification and canary rollouts.",
            "Maintain immutable, air-gapped backups to guarantee recovery without negotiating with extortionists."
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source.name if self.source else "Cyber Intelligence",
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "category": self.category,
            "severity": self.severity,
            "financial_impact": self.financial_impact,
            "summary": self.effective_what_happened_easy,
            "what_happened": self.what_happened_en or self.effective_what_happened_easy,
            "who_is_affected": self.effective_who_is_affected,
            "why_it_matters": self.effective_why_it_matters,
            "what_to_do": self.what_to_do_en or "\n".join(self.effective_cure_remediation),
            "cure_remediation": self.effective_cure_remediation,
            "lessons_learned": self.effective_lessons_learned,
            "technical_analysis": self.meta.get("technical_analysis", {}),
            "behavioral_analysis": self.meta.get("behavioral_analysis", {}),
            "key_takeaways": self.effective_lessons_learned,
            "is_breaking": self.is_breaking,
        }


class CommunityPost(db.Model, TimestampMixin):
    __tablename__ = "community_posts"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    group_name = db.Column(db.String(120))
    topic = db.Column(db.String(160), index=True)
    body = db.Column(db.Text, nullable=False)
    is_hidden = db.Column(db.Boolean, default=False, nullable=False)
    report_count = db.Column(db.Integer, default=0, nullable=False)


class ModerationReport(db.Model):
    __tablename__ = "moderation_reports"

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    post_id = db.Column(
        db.Integer, db.ForeignKey("community_posts.id", ondelete="CASCADE")
    )
    reason = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(24), default="open", nullable=False, index=True)
    handled_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
