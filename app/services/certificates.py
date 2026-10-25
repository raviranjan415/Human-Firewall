"""Certificate eligibility, issuance, PDF rendering and public verification."""

from __future__ import annotations

import io
import secrets

from flask import current_app, url_for

from app.extensions import db
from app.models import Certificate, User
from app.models.progress import CERTIFICATE_TIERS
from app.services import gamification
from app.services import labs as labs_service

TIER_ORDER = ("basic", "intermediate", "advanced", "master")


def eligibility(user: User, tier: str) -> dict:
    """Check a tier's prerequisites. Certificates are only issued when the
    backend confirms eligibility — the frontend never decides this."""
    info = CERTIFICATE_TIERS.get(tier)
    if info is None:
        return {"eligible": False, "reason": "unknown_tier", "tier": tier}

    passed = labs_service.passed_lab_ids(user)
    required = info["required_labs"]
    if len(passed) < required:
        return {
            "eligible": False,
            "reason": "labs",
            "tier": tier,
            "required_labs": required,
            "completed_labs": len(passed),
            "remaining": required - len(passed),
        }

    existing = Certificate.query.filter_by(user_id=user.id, tier=tier, revoked=False).first()
    if existing:
        return {"eligible": False, "reason": "already_issued", "tier": tier,
                "certificate": existing}

    return {
        "eligible": True,
        "reason": None,
        "tier": tier,
        "required_labs": required,
        "completed_labs": len(passed),
    }


def all_eligibility(user: User) -> list[dict]:
    return [eligibility(user, tier) for tier in TIER_ORDER]


def _generate_uid() -> str:
    return "CQ-" + secrets.token_hex(6).upper()


def _generate_code() -> str:
    return secrets.token_hex(4).upper()


def issue_certificate(user: User, tier: str, score_percentage: int | None = None) -> dict:
    """Issue a certificate inside a single transaction.

    The ``uq_certificate_tier_per_user`` constraint guarantees a learner can
    never hold two certificates for the same tier.
    """
    state = eligibility(user, tier)
    if not state["eligible"]:
        return state

    stats = gamification.user_stats(user)
    certificate = Certificate(
        certificate_uid=_generate_uid(),
        verification_code=_generate_code(),
        user_id=user.id,
        tier=tier,
        learner_name=user.name,
        score_percentage=int(
            score_percentage
            if score_percentage is not None
            else min(100, max(0, stats["labs_completed"]))
        ),
        labs_completed=stats["labs_completed"],
    )
    db.session.add(certificate)
    try:
        db.session.commit()
    except Exception:  # pragma: no cover - unique race
        db.session.rollback()
        return {"eligible": False, "reason": "already_issued", "tier": tier}

    gamification.award_xp(
        user,
        CERTIFICATE_TIERS[tier]["xp"],
        reason="certificate",
        reference_type="certificate",
        reference_id=certificate.certificate_uid,
    )
    gamification.log_event(user.id, "certificate_issued", "certificate", certificate.id,
                           payload={"tier": tier})
    db.session.commit()
    gamification.evaluate_achievements(user)
    db.session.commit()
    return {"eligible": True, "certificate": certificate, "reason": None, "tier": tier}


def verify(code: str) -> dict | None:
    """Public verification: reveals only the minimum necessary information."""
    certificate = Certificate.query.filter_by(verification_code=(code or "").strip().upper()).first()
    if certificate is None or certificate.revoked:
        return None
    return {
        "learner_name": certificate.learner_name,
        "tier": certificate.tier,
        "tier_name": CERTIFICATE_TIERS.get(certificate.tier, {}).get("name", certificate.tier),
        "issued_at": certificate.issued_at,
        "certificate_uid": certificate.certificate_uid,
        "labs_completed": certificate.labs_completed,
        "issuer": "Human Firewall Cyber Resilience Platform",
    }


def build_pdf(certificate: Certificate) -> bytes:
    """Render a PDF certificate with a verification QR code."""
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as pdf_canvas

    from reportlab.lib.utils import ImageReader

    tier_name = CERTIFICATE_TIERS.get(certificate.tier, {}).get("name", certificate.tier.title())

    try:
        verification_url = url_for(
            "certificates.verify_page", code=certificate.verification_code, _external=True
        )
    except Exception:  # pragma: no cover - outside request context
        verification_url = (
            f"https://humanfirewall.example/certificates/verify/{certificate.verification_code}"
        )

    buffer = io.BytesIO()
    page = pdf_canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Background
    page.setFillColorRGB(0.03, 0.07, 0.18)
    page.rect(0, 0, width, height, stroke=0, fill=1)

    # Border
    page.setStrokeColorRGB(0.13, 0.83, 1.0)
    page.setLineWidth(3)
    page.rect(12 * mm, 12 * mm, width - 24 * mm, height - 24 * mm, stroke=1, fill=0)
    page.setStrokeColorRGB(0.55, 0.36, 0.96)
    page.setLineWidth(1)
    page.rect(16 * mm, 16 * mm, width - 32 * mm, height - 32 * mm, stroke=1, fill=0)

    # Header
    page.setFillColorRGB(0.13, 0.83, 1.0)
    page.setFont("Helvetica-Bold", 30)
    page.drawCentredString(width / 2, height - 45 * mm, "Human Firewall")
    page.setFillColorRGB(0.85, 0.9, 1.0)
    page.setFont("Helvetica", 13)
    page.drawCentredString(width / 2, height - 55 * mm, "Defensive Cybersecurity Awareness & Gamified Learning")

    page.setFillColorRGB(1, 1, 1)
    page.setFont("Helvetica-Bold", 19)
    page.drawCentredString(width / 2, height - 75 * mm, "Certificate of Completion")
    page.setFont("Helvetica", 14)
    page.setFillColorRGB(0.6, 0.9, 1.0)
    page.drawCentredString(width / 2, height - 88 * mm, tier_name)

    page.setFillColorRGB(1, 1, 1)
    page.setFont("Helvetica", 12)
    page.drawCentredString(width / 2, height - 108 * mm, "This certifies that")
    page.setFont("Helvetica-Bold", 26)
    page.setFillColorRGB(0.13, 0.83, 1.0)
    page.drawCentredString(width / 2, height - 122 * mm, certificate.learner_name)
    page.setFillColorRGB(0.85, 0.9, 1.0)
    page.setFont("Helvetica", 12)
    page.drawCentredString(
        width / 2,
        height - 136 * mm,
        f"completed {certificate.labs_completed} validated practical labs "
        f"with an assessed score of {certificate.score_percentage}%.",
    )

    # Metadata
    page.setFont("Helvetica", 10)
    page.setFillColorRGB(0.72, 0.78, 0.9)
    page.drawString(
        25 * mm, 30 * mm,
        f"Certificate ID: {certificate.certificate_uid}    "
        f"Issued: {certificate.issued_at.strftime('%d %b %Y')}    "
        f"Verification code: {certificate.verification_code}",
    )
    page.drawString(
        25 * mm, 25 * mm,
        "Platform training record — not an accredited professional certification.",
    )

    # Signature line
    page.setStrokeColorRGB(0.5, 0.6, 0.8)
    page.setLineWidth(0.7)
    page.line(width - 85 * mm, 33 * mm, width - 30 * mm, 33 * mm)
    page.setFont("Helvetica", 9)
    page.drawCentredString(width - 57.5 * mm, 28 * mm, "CyberQuest Programme Office")

    # QR code
    try:
        import qrcode

        qr = qrcode.QRCode(box_size=3, border=1)
        qr.add_data(verification_url)
        qr.make(fit=True)
        image = qr.make_image(fill_color="white", back_color="#081229").convert("RGB")
        qr_buffer = io.BytesIO()
        image.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        page.drawImage(
            ImageReader(qr_buffer),
            width - 55 * mm,
            40 * mm,
            width=28 * mm,
            height=28 * mm,
            preserveAspectRatio=True,
            mask="auto",
        )
    except Exception:  # pragma: no cover - optional dependency
        current_app.logger.warning("QR code generation unavailable for certificates.")

    page.showPage()
    page.save()
    return buffer.getvalue()
