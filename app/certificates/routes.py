"""Certificate issuance, download and public verification.

Eligibility is always re-checked on the server. A learner can never issue a
certificate by manipulating the request.
"""

from __future__ import annotations

import io

from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from app.models import Certificate
from app.models.progress import CERTIFICATE_TIERS
from app.services import certificates as certificates_service

certificates_bp = Blueprint("certificates", __name__)


@certificates_bp.route("/")
@login_required
def index():
    certificates = (
        Certificate.query.filter_by(user_id=current_user.id)
        .order_by(Certificate.issued_at.desc())
        .all()
    )
    return render_template(
        "certificates/index.html",
        certificates=certificates,
        eligibility=certificates_service.all_eligibility(current_user),
        tiers=CERTIFICATE_TIERS,
    )


@certificates_bp.route("/issue/<tier>", methods=["POST"])
@login_required
def issue(tier: str):
    if tier not in CERTIFICATE_TIERS:
        abort(404)

    result = certificates_service.issue_certificate(current_user, tier)
    if result.get("eligible"):
        flash("Certificate issued. Congratulations!", "success")
    elif result.get("reason") == "already_issued":
        flash("You already hold that certificate.", "info")
    else:
        remaining = result.get("remaining")
        flash(
            f"Not eligible yet — {remaining} more labs to pass." if remaining else
            "Not eligible yet.",
            "error",
        )
    return redirect(url_for("certificates.index"))


@certificates_bp.route("/<int:certificate_id>/download")
@login_required
def download(certificate_id: int):
    certificate = Certificate.query.filter_by(
        id=certificate_id, user_id=current_user.id, revoked=False
    ).first_or_404()

    pdf_bytes = certificates_service.build_pdf(certificate)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"cyberquest-{certificate.tier}-{certificate.verification_code}.pdf",
    )


@certificates_bp.route("/verify")
def verify():
    """Public verification form. Accepts a code by query string or POST."""
    code = (request.values.get("code") or "").strip().upper()
    result = certificates_service.verify(code) if code else None
    return render_template("certificates/verify.html", code=code, result=result)


@certificates_bp.route("/verify/<code>")
def verify_page(code: str):
    """Verification result page — the QR code on every PDF points here."""
    code = (code or "").strip().upper()
    result = certificates_service.verify(code)
    return render_template("certificates/verify_page.html", code=code, result=result)
