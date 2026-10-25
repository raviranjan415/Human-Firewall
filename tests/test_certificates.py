"""Certificate eligibility, issuance, PDF rendering and public verification."""

from __future__ import annotations

from app.models import Certificate, Lab, LabAttempt, User
from app.models.progress import CERTIFICATE_TIERS
from app.services import certificates as certificates_service

from .conftest import ADMIN_PASSWORD, ADMIN_USERNAME, login


def pass_n_labs(lab_ids, user, db) -> None:
    for lab_id in lab_ids:
        db.session.add(
            LabAttempt(
                user_id=user.id,
                lab_id=lab_id,
                percentage=100,
                score=100,
                max_score=100,
                passed=True,
                status="passed",
                hints_used=0,
            )
        )
    db.session.commit()


def lab_ids_up_to(count: int) -> list[int]:
    rows = (
        Lab.query.filter(Lab.number <= count)
        .order_by(Lab.number)
        .with_entities(Lab.id)
        .all()
    )
    return [row[0] for row in rows]


def test_eligibility_is_refused_without_enough_labs(app, learner):
    state = certificates_service.eligibility(learner, "basic")
    assert state["eligible"] is False
    assert state["reason"] == "labs"
    assert state["required_labs"] == CERTIFICATE_TIERS["basic"]["required_labs"]
    assert state["remaining"] == CERTIFICATE_TIERS["basic"]["required_labs"]


def test_unknown_tier_is_never_eligible(app, learner):
    state = certificates_service.eligibility(learner, "platinum")
    assert state["eligible"] is False
    assert state["reason"] == "unknown_tier"


def test_certificate_is_issued_only_once_the_backend_confirms_eligibility(app, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)

    result = certificates_service.issue_certificate(learner, "basic")
    assert result["eligible"] is True
    certificate = result["certificate"]
    assert certificate.verification_code
    assert certificate.certificate_uid.startswith("CQ-")
    assert certificate.learner_name == learner.name

    again = certificates_service.issue_certificate(learner, "basic")
    assert again["eligible"] is False
    assert again["reason"] == "already_issued"
    assert Certificate.query.filter_by(user_id=learner.id, tier="basic").count() == 1


def test_issuing_a_certificate_pays_the_tier_xp_once(app, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    certificates_service.issue_certificate(learner, "basic")
    db.session.expire_all()
    after_first = User.query.get(learner.id).xp_total

    certificates_service.issue_certificate(learner, "basic")
    db.session.expire_all()
    assert User.query.get(learner.id).xp_total == after_first
    assert after_first >= CERTIFICATE_TIERS["basic"]["xp"]


def test_higher_tiers_need_more_labs(app, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    assert certificates_service.eligibility(learner, "basic")["eligible"] is True
    assert certificates_service.eligibility(learner, "intermediate")["eligible"] is False
    assert certificates_service.eligibility(learner, "advanced")["eligible"] is False
    assert certificates_service.eligibility(learner, "master")["eligible"] is False


def test_verification_reveals_only_the_certificate_holder(app, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    certificate = certificates_service.issue_certificate(learner, "basic")["certificate"]

    info = certificates_service.verify(certificate.verification_code.lower())
    assert info is not None
    assert info["learner_name"] == learner.name
    assert info["tier"] == "basic"
    assert info["certificate_uid"] == certificate.certificate_uid
    assert "email" not in info
    assert "user_id" not in info


def test_revoked_and_unknown_certificates_do_not_verify(app, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    certificate = certificates_service.issue_certificate(learner, "basic")["certificate"]

    assert certificates_service.verify("NOPE1234") is None

    certificate.revoked = True
    db.session.commit()
    assert certificates_service.verify(certificate.verification_code) is None


def test_pdf_is_generated_with_a_qr_code(app, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    certificate = certificates_service.issue_certificate(learner, "basic")["certificate"]

    pdf = certificates_service.build_pdf(certificate)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 2000


def test_verify_page_is_public(client, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    certificate = certificates_service.issue_certificate(learner, "basic")["certificate"]

    response = client.get(f"/certificates/verify/{certificate.verification_code}")
    assert response.status_code == 200
    assert learner.name in response.get_data(as_text=True)


def test_cannot_issue_a_certificate_over_http_without_eligibility(client, learner):
    login(client, "learner1")
    response = client.post("/certificates/issue/basic", follow_redirects=True)
    assert response.status_code == 200
    assert Certificate.query.filter_by(user_id=learner.id).count() == 0
    assert b"Not eligible" in response.data


def test_issue_and_download_over_http(client, learner, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    login(client, "learner1")

    client.post("/certificates/issue/basic", follow_redirects=True)
    certificate = Certificate.query.filter_by(user_id=learner.id, tier="basic").first()
    assert certificate is not None

    download = client.get(f"/certificates/{certificate.id}/download")
    assert download.status_code == 200
    assert download.headers["Content-Type"].startswith("application/pdf")
    assert download.data.startswith(b"%PDF")


def test_a_learner_cannot_download_someone_elses_certificate(client, learner, instructor, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    certificate = certificates_service.issue_certificate(learner, "basic")["certificate"]

    login(client, "instructor1")
    assert client.get(f"/certificates/{certificate.id}/download").status_code == 404


def test_certificate_page_requires_authentication(client):
    response = client.get("/certificates/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_certificate_tiers_are_ordered(app):
    required = [CERTIFICATE_TIERS[t]["required_labs"] for t in ("basic", "intermediate", "advanced", "master")]
    assert required == sorted(required)
    assert required[-1] == 100


def test_admin_can_see_the_certificate_inventory(client, learner, admin_user, db):
    pass_n_labs(lab_ids_up_to(30), learner, db)
    certificates_service.issue_certificate(learner, "basic")

    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    assert client.get("/admin/").status_code == 200
