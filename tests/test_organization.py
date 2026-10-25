"""Automated test suite for Human Firewall Organization & Multi-Tenant Features.

Tests cover:
- Organization creation, code generation, and rotation
- Pre-approved eligible member registry and CSV import
- Automated 5-step enrollment verification workflow
- Seat limit enforcement and enrollment passcodes
- Existing personal user account linking without data loss
- Strict tenant isolation across organizations and roles
- Audited HR-assisted account recovery
- Organization-scoped CSV and PDF compliance reports
"""

from __future__ import annotations

import io
import pytest
from flask import url_for

from app.extensions import db
from app.models import (
    AccountRecoveryCode,
    EligibleMember,
    Organization,
    OrganizationMembership,
    Role,
    User,
)
from app.models.organization import (
    ORG_ROLE_ADMIN,
    ORG_ROLE_MEMBER,
    PLAN_STARTER,
    STATUS_ACTIVE,
    STATUS_ELIGIBLE,
)
from app.models.user import ROLE_LEARNER, ROLE_ORG_ADMIN
from app.services import organizations as org_service
from .conftest import LEARNER_PASSWORD, login


@pytest.fixture
def org_admin(app, make_user):
    admin = make_user("hr_admin_1", role=ROLE_ORG_ADMIN, email="hr1@apexcorp.test")
    return admin


@pytest.fixture
def other_admin(app, make_user):
    admin = make_user("hr_admin_2", role=ROLE_ORG_ADMIN, email="hr2@otheruniv.test")
    return admin


@pytest.fixture
def sample_org(app, org_admin):
    org = org_service.create_organization(
        name="Apex Cyber Solutions",
        plan_code=PLAN_STARTER,
        seats=10,
        admin_user=org_admin,
    )
    return org


@pytest.fixture
def other_org(app, other_admin):
    org = org_service.create_organization(
        name="Metro Technical University",
        plan_code=PLAN_STARTER,
        seats=10,
        admin_user=other_admin,
    )
    return org


# ---------------------------------------------------------------------------
# 1. Organization Creation & Code Generation / Rotation
# ---------------------------------------------------------------------------

def test_organization_creation_generates_unique_code(app, org_admin):
    org = org_service.create_organization(
        name="Security First Inc",
        plan_code=PLAN_STARTER,
        seats=25,
        admin_user=org_admin,
    )
    assert org.id is not None
    assert org.org_code.startswith("HF-")
    assert org.seats_purchased == 25
    assert org.occupied_seats == 1  # admin is enrolled as member
    assert len(org.subscriptions) > 0
    assert org.subscriptions[0].status == "active"


def test_organization_code_rotation(app, sample_org, org_admin):
    old_code = sample_org.org_code
    new_code = org_service.rotate_organization_code(sample_org, actor=org_admin)
    assert new_code != old_code
    assert new_code.startswith("HF-")
    assert sample_org.org_code == new_code


# ---------------------------------------------------------------------------
# 2. Pre-Approved Eligible Registry & CSV Import
# ---------------------------------------------------------------------------

def test_csv_eligible_registry_import(app, sample_org, org_admin):
    csv_content = (
        "registration_id,full_name,email,department\n"
        "EMP-1001,Alice Smith,alice@apexcorp.test,SecOps\n"
        "EMP-1002,Bob Jones,bob@apexcorp.test,Finance\n"
        "EMP-1001,Alice Duplicate,alice2@apexcorp.test,SecOps\n"  # Duplicate in CSV
        ",Malformed Row Missing ID,no-id@test.com,HR\n"           # Missing ID
    )
    result = org_service.import_eligible_members_csv(sample_org, csv_content, actor=org_admin)
    
    assert result["success"] is True
    assert result["created_count"] == 2
    assert result["rejected_count"] == 2

    reg1 = EligibleMember.query.filter_by(organization_id=sample_org.id, identifier="EMP-1001").first()
    assert reg1 is not None
    assert reg1.full_name == "Alice Smith"
    assert reg1.status == STATUS_ELIGIBLE


def test_eligible_member_registry_is_scoped_to_organization(app, sample_org, other_org):
    # Two different organizations can legitimately have the same identifier (e.g. EMP-999)
    db.session.add(EligibleMember(organization_id=sample_org.id, identifier="EMP-999", full_name="User Org A"))
    db.session.add(EligibleMember(organization_id=other_org.id, identifier="EMP-999", full_name="User Org B"))
    db.session.commit()

    assert EligibleMember.query.filter_by(identifier="EMP-999").count() == 2


# ---------------------------------------------------------------------------
# 3. Automated 5-Step Enrollment Workflow
# ---------------------------------------------------------------------------

def test_automated_enrollment_happy_path(client, sample_org):
    # Pre-approve identifier
    db.session.add(EligibleMember(
        organization_id=sample_org.id,
        identifier="EMP-2001",
        full_name="Carol Danvers",
        approved_email="carol@example.com",
        status=STATUS_ELIGIBLE,
    ))
    db.session.commit()

    initial_occupied = sample_org.occupied_seats

    resp = client.post("/auth/enroll", data={
        "org_code": sample_org.org_code,
        "registration_id": "EMP-2001",
        "username": "carol_sec",
        "email": "carol@example.com",
        "display_name": "Carol Danvers",
        "password": "CarolPassword123!",
        "confirm_password": "CarolPassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)

    assert resp.status_code == 200
    user = User.query.filter_by(username="carol_sec").first()
    assert user is not None
    assert user.email == "carol@example.com"

    # Membership established
    membership = OrganizationMembership.query.filter_by(
        organization_id=sample_org.id, user_id=user.id
    ).first()
    assert membership is not None
    assert membership.status == STATUS_ACTIVE
    assert membership.registration_id == "EMP-2001"

    # Registry marked as active
    reg_record = EligibleMember.query.filter_by(
        organization_id=sample_org.id, identifier="EMP-2001"
    ).first()
    assert reg_record.status == STATUS_ACTIVE
    assert reg_record.claimed_by_user_id == user.id

    # Seat occupied count incremented
    db.session.refresh(sample_org)
    assert sample_org.occupied_seats == initial_occupied + 1


def test_enrollment_rejected_with_invalid_org_code(client, sample_org):
    resp = client.post("/auth/enroll", data={
        "org_code": "HF-INVALID-9999",
        "registration_id": "EMP-2001",
        "username": "bad_code_user",
        "email": "badcode@test.com",
        "password": "CarolPassword123!",
        "confirm_password": "CarolPassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)
    assert b"Invalid Organization Code" in resp.data
    assert User.query.filter_by(username="bad_code_user").first() is None


def test_enrollment_rejected_when_not_in_eligible_registry(client, sample_org):
    resp = client.post("/auth/enroll", data={
        "org_code": sample_org.org_code,
        "registration_id": "UNAUTHORIZED-ID-999",
        "username": "unauthorized_user",
        "email": "unauth@example.com",
        "password": "CarolPassword123!",
        "confirm_password": "CarolPassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)
    assert b"could not be verified" in resp.data
    assert User.query.filter_by(username="unauthorized_user").first() is None


def test_enrollment_prevents_double_claiming_identifier(client, sample_org):
    # Pre-approve identifier
    db.session.add(EligibleMember(
        organization_id=sample_org.id,
        identifier="EMP-2002",
        full_name="David Banner",
        status=STATUS_ELIGIBLE,
    ))
    db.session.commit()

    # User 1 successfully enrolls
    client.post("/auth/enroll", data={
        "org_code": sample_org.org_code,
        "registration_id": "EMP-2002",
        "username": "david_banner",
        "email": "david@example.com",
        "password": "DavidPassword123!",
        "confirm_password": "DavidPassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)

    # Log out User 1 so client can attempt enrollment as User 2
    client.post("/auth/logout", follow_redirects=True)

    # User 2 attempts to claim the same identifier
    resp2 = client.post("/auth/enroll", data={
        "org_code": sample_org.org_code,
        "registration_id": "EMP-2002",
        "username": "david_impostor",
        "email": "impostor@example.com",
        "password": "DavidPassword123!",
        "confirm_password": "DavidPassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)

    assert b"already been claimed" in resp2.data
    assert User.query.filter_by(username="david_impostor").first() is None


def test_enrollment_passcode_validation(client, sample_org):
    # Enable enrollment passcode
    sample_org.set_passcode("SecretPass2026!")
    db.session.add(EligibleMember(
        organization_id=sample_org.id,
        identifier="EMP-PASS-1",
        status=STATUS_ELIGIBLE,
    ))
    db.session.commit()

    # Wrong passcode
    resp_wrong = client.post("/auth/enroll", data={
        "org_code": sample_org.org_code,
        "registration_id": "EMP-PASS-1",
        "passcode": "WrongSecret",
        "username": "pass_tester",
        "email": "pass_tester@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)
    assert b"Invalid enrollment passcode" in resp_wrong.data

    # Correct passcode
    resp_ok = client.post("/auth/enroll", data={
        "org_code": sample_org.org_code,
        "registration_id": "EMP-PASS-1",
        "passcode": "SecretPass2026!",
        "username": "pass_tester",
        "email": "pass_tester@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)
    assert resp_ok.status_code == 200
    assert User.query.filter_by(username="pass_tester").first() is not None


def test_seat_limit_enforcement(client, org_admin):
    # Create org with exactly 1 purchased seat (admin occupies it)
    tight_org = org_service.create_organization(
        name="Small Firm LLC",
        plan_code=PLAN_STARTER,
        seats=1,
        admin_user=org_admin,
    )
    assert tight_org.available_seats == 0

    db.session.add(EligibleMember(
        organization_id=tight_org.id,
        identifier="EMP-TIGHT-1",
        status=STATUS_ELIGIBLE,
    ))
    db.session.commit()

    resp = client.post("/auth/enroll", data={
        "org_code": tight_org.org_code,
        "registration_id": "EMP-TIGHT-1",
        "username": "tight_user",
        "email": "tight@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
        "accept_terms": "y",
    }, follow_redirects=True)

    assert b"occupied" in resp.data.lower() or b"capacity" in resp.data.lower()
    assert User.query.filter_by(username="tight_user").first() is None


# ---------------------------------------------------------------------------
# 4. Existing Personal User Joining an Organization (Account Linking)
# ---------------------------------------------------------------------------

def test_existing_personal_account_joins_organization(client, sample_org, make_user):
    # Personal learner with existing XP and progress
    personal_user = make_user("eva_learner", email="eva@personal.test", password="EvaPassword123!")
    personal_user.xp_total = 750
    db.session.commit()

    # Org pre-approves Eva's student ID
    db.session.add(EligibleMember(
        organization_id=sample_org.id,
        identifier="STU-8822",
        approved_email="eva@personal.test",
        status=STATUS_ELIGIBLE,
    ))
    db.session.commit()

    # Eva logs into her personal account
    login(client, "eva_learner", "EvaPassword123!")

    # Eva navigates to Join Org
    resp = client.post("/auth/join-org", data={
        "org_code": sample_org.org_code,
        "registration_id": "STU-8822",
    }, follow_redirects=True)

    assert resp.status_code == 200

    # Eva retains her personal user ID and XP
    db.session.refresh(personal_user)
    assert personal_user.xp_total == 750
    assert personal_user.email == "eva@personal.test"
    assert personal_user.active_organization.id == sample_org.id

    membership = personal_user.get_membership(sample_org.id)
    assert membership is not None
    assert membership.registration_id == "STU-8822"


# ---------------------------------------------------------------------------
# 5. Multi-Tenant Isolation & Role Authorization
# ---------------------------------------------------------------------------

def test_tenant_isolation_cross_org_access_blocked(client, sample_org, other_org, org_admin, other_admin):
    # Log in as Admin of Org A (Apex)
    login(client, org_admin.username, LEARNER_PASSWORD)

    # Attempt to access Org B's HR dashboard
    resp = client.get(f"/org/{other_org.id}/dashboard")
    assert resp.status_code in (403, 302)

    # Attempt to access Org B's eligible member registry
    resp_registry = client.get(f"/org/{other_org.id}/eligible")
    assert resp_registry.status_code in (403, 302)

    # Org A admin CAN access Org A's dashboard
    resp_own = client.get(f"/org/{sample_org.id}/dashboard")
    assert resp_own.status_code == 200
    assert b"Apex Cyber Solutions" in resp_own.data


def test_regular_learner_cannot_access_hr_dashboard(client, sample_org, make_user):
    learner = make_user("frank_student", email="frank@univ.test", password="FrankPassword123!")
    org_service.establish_membership(
        user=learner,
        org=sample_org,
        role=ORG_ROLE_MEMBER,
        registration_id="STU-FRANK",
    )

    login(client, learner.username, "FrankPassword123!")

    resp = client.get(f"/org/{sample_org.id}/dashboard")
    assert resp.status_code in (403, 302)


# ---------------------------------------------------------------------------
# 6. Audited HR-Assisted Account Recovery
# ---------------------------------------------------------------------------

def test_hr_assisted_account_recovery_workflow(client, sample_org, other_org, org_admin, other_admin, make_user):
    # Member in Org A who lost email access
    locked_member = make_user("locked_user", email="lost_inbox@apexcorp.test", password="OldPassword123!")
    org_service.establish_membership(
        user=locked_member,
        org=sample_org,
        role=ORG_ROLE_MEMBER,
        registration_id="EMP-LOCKED",
    )

    # Org Admin A generates recovery code
    raw_code, err = org_service.initiate_hr_account_recovery(
        org=sample_org,
        target_user=locked_member,
        actor=org_admin,
    )
    assert err is None
    assert raw_code is not None
    assert raw_code.startswith("HF-REC-")

    # Verify that Admin B cannot generate recovery code for Org A's member
    code_b, err_b = org_service.initiate_hr_account_recovery(
        org=other_org,
        target_user=locked_member,
        actor=other_admin,
    )
    assert code_b is None
    assert "Unauthorized" in err_b or "Target user is not" in err_b

    # Locked member redeems code via public recovery endpoint
    resp_redeem = client.post("/auth/recover", data={
        "recovery_code": raw_code,
        "password": "NewSecurePassword2026!",
        "confirm_password": "NewSecurePassword2026!",
    }, follow_redirects=True)
    assert b"successfully reset" in resp_redeem.data

    # Code cannot be re-used (anti-replay)
    resp_replay = client.post("/auth/recover", data={
        "recovery_code": raw_code,
        "password": "AnotherPassword123!",
        "confirm_password": "AnotherPassword123!",
    }, follow_redirects=True)
    assert b"invalid or expired" in resp_replay.data.lower()

    # User can now sign in with the new password
    login_resp = login(client, "locked_user", "NewSecurePassword2026!")
    assert login_resp.status_code == 200


# ---------------------------------------------------------------------------
# 7. Compliance Report Exports (CSV & PDF)
# ---------------------------------------------------------------------------

def test_organization_report_exports(client, sample_org, org_admin):
    login(client, org_admin.username, LEARNER_PASSWORD)

    # CSV Export
    resp_csv = client.get(f"/org/{sample_org.id}/reports/export.csv")
    assert resp_csv.status_code == 200
    assert "text/csv" in resp_csv.content_type
    assert b"Username" in resp_csv.data
    assert b"hr_admin_1" in resp_csv.data

    # PDF Export
    resp_pdf = client.get(f"/org/{sample_org.id}/reports/summary.pdf")
    assert resp_pdf.status_code == 200
    assert "application/pdf" in resp_pdf.content_type
    assert resp_pdf.data.startswith(b"%PDF")
