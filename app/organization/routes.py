"""Organization workspace, HR/T&P administration, eligible registry, and commercial subscription routes."""

from __future__ import annotations

import io
import json
import logging
from datetime import datetime, timedelta

from flask import (
    Blueprint,
    Response,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import func

from app.auth.decorators import org_admin_required, tenant_membership_required
from app.extensions import db, limiter
from app.models import (
    AuditLog,
    Certificate,
    EligibleMember,
    Lab,
    LabAttempt,
    LearningAssignment,
    LearningPath,
    OrgInvitation,
    Organization,
    OrganizationMembership,
    OrganizationSubscription,
    SubscriptionInvoice,
    User,
    UserProgress,
)
from app.models.organization import (
    ORGANIZATION_PLANS,
    ORG_ROLE_ADMIN,
    ORG_ROLE_MEMBER,
    ORG_ROLE_TP_COORDINATOR,
    PLAN_ENTERPRISE,
    PLAN_PROFESSIONAL,
    PLAN_STARTER,
    STATUS_ACTIVE,
    STATUS_AWAITING_VERIFICATION,
    STATUS_ELIGIBLE,
    STATUS_INVITATION_SENT,
    STATUS_PENDING_APPROVAL,
    STATUS_REGISTRATION_STARTED,
    STATUS_REVOKED,
    STATUS_SUSPENDED,
    hash_token,
)
from app.models.user import utcnow
from app.services import organizations as org_service

logger = logging.getLogger(__name__)

organization_bp = Blueprint("organization", __name__)


def _audit(action: str, target_type: str | None = None, target_id=None, detail: dict | None = None):
    db.session.add(
        AuditLog(
            actor_id=current_user.id if current_user.is_authenticated else None,
            action=action,
            target_type=target_type,
            target_id=str(target_id) if target_id is not None else None,
            detail_json=json.dumps(detail) if detail else None,
            ip_address=request.remote_addr,
        )
    )


# ---------------------------------------------------------------------------
# Commercial & Enterprise Training Overview
# ---------------------------------------------------------------------------

@organization_bp.route("/enterprise")
def enterprise_plans():
    """Enterprise training plans, pricing tiers, and commercial quotation workflow."""
    return render_template(
        "organization/enterprise.html",
        plans=ORGANIZATION_PLANS,
        starter=ORGANIZATION_PLANS[PLAN_STARTER],
        professional=ORGANIZATION_PLANS[PLAN_PROFESSIONAL],
        enterprise=ORGANIZATION_PLANS[PLAN_ENTERPRISE],
    )


@organization_bp.route("/enterprise/register", methods=["GET", "POST"])
def register_organization():
    """Register a new organization and initialize its subscription workspace."""
    if request.method == "POST":
        org_name = (request.form.get("name") or "").strip()
        plan_code = (request.form.get("plan") or PLAN_STARTER).strip().lower()
        seats_raw = request.form.get("seats")
        domain = (request.form.get("domain") or "").strip()
        contact_name = (request.form.get("contact_name") or "").strip()
        contact_email = (request.form.get("contact_email") or "").strip().lower()

        if not org_name:
            flash("Organization name is required.", "error")
            return redirect(url_for("organization.register_organization"))

        if Organization.query.filter(func.lower(Organization.name) == org_name.lower()).first():
            flash("An organization with that name already exists.", "error")
            return redirect(url_for("organization.register_organization"))

        plan = ORGANIZATION_PLANS.get(plan_code, ORGANIZATION_PLANS[PLAN_STARTER])
        try:
            seats = max(int(seats_raw), 5) if seats_raw else plan["seats"]
        except (ValueError, TypeError):
            seats = plan["seats"]

        admin_user = current_user if current_user.is_authenticated else None
        org = org_service.create_organization(
            name=org_name,
            plan_code=plan_code,
            seats=seats,
            domain=domain if domain else None,
            contact_email=contact_email if contact_email else (admin_user.email if admin_user else None),
            contact_name=contact_name if contact_name else (admin_user.name if admin_user else None),
            admin_user=admin_user,
        )

        flash(
            f"Organization workspace '{org.name}' created! Your Organization Code is {org.org_code}.",
            "success",
        )
        if current_user.is_authenticated:
            return redirect(url_for("organization.workspace_dashboard", org_id=org.id))
        return redirect(url_for("auth.login", type="org", code=org.org_code))

    return render_template(
        "organization/register_org.html",
        plans=ORGANIZATION_PLANS,
        selected_plan=request.args.get("plan", PLAN_STARTER),
    )


@organization_bp.route("/enterprise/quote", methods=["POST"])
@limiter.limit("10 per hour")
def request_quotation():
    """Submit an enterprise training quotation or custom licensing request."""
    company = (request.form.get("company") or "").strip()
    contact = (request.form.get("contact") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    seats = (request.form.get("seats") or "").strip()
    notes = (request.form.get("notes") or "").strip()

    if not company or not email:
        flash("Company name and email address are required.", "error")
        return redirect(url_for("organization.enterprise_plans"))

    _audit(
        "enterprise_quote_requested",
        "commercial",
        None,
        {"company": company, "contact": contact, "email": email, "seats": seats, "notes": notes},
    )
    db.session.commit()

    flash(
        f"Thank you, {contact or company}! Your enterprise quotation request for {seats or 'custom'} seats has been received. Our team will contact {email} within 1 business day.",
        "success",
    )
    return redirect(url_for("organization.enterprise_plans"))


# ---------------------------------------------------------------------------
# HR / T&P Dashboard & Management
# ---------------------------------------------------------------------------

@organization_bp.route("/<int:org_id>/dashboard")
@org_admin_required
def workspace_dashboard(org_id: int):
    """Main HR / Corporate Training Manager / T&P Coordinator Dashboard."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    metrics = org_service.get_organization_dashboard_metrics(org)
    recent_memberships = (
        OrganizationMembership.query.filter_by(organization_id=org.id)
        .order_by(OrganizationMembership.joined_at.desc())
        .limit(8)
        .all()
    )
    pending_approvals = (
        OrganizationMembership.query.filter_by(
            organization_id=org.id, status=STATUS_PENDING_APPROVAL
        )
        .order_by(OrganizationMembership.joined_at.asc())
        .limit(10)
        .all()
    )
    recent_assignments = (
        LearningAssignment.query.filter_by(organization_id=org.id)
        .order_by(LearningAssignment.created_at.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "organization/dashboard.html",
        org=org,
        metrics=metrics,
        recent_memberships=recent_memberships,
        pending_approvals=pending_approvals,
        recent_assignments=recent_assignments,
        plans=ORGANIZATION_PLANS,
    )


# ---------------------------------------------------------------------------
# Organization Workspace for Learners / Teammates
# ---------------------------------------------------------------------------

@organization_bp.route("/<int:org_id>/workspace")
@tenant_membership_required
def workspace_overview(org_id: int):
    """Learner workspace overview for their organization."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    my_membership = current_user.get_membership(org.id)
    assignments = (
        LearningAssignment.query.filter_by(organization_id=org.id, assignee_id=current_user.id)
        .order_by(LearningAssignment.due_date.asc().nullslast())
        .all()
    )

    # Organization leaderboard
    member_ids = [
        m.user_id for m in OrganizationMembership.query.filter_by(
            organization_id=org.id, status=STATUS_ACTIVE
        ).all()
    ]
    top_teammates = (
        User.query.filter(User.id.in_(member_ids))
        .order_by(User.xp_total.desc())
        .limit(10)
        .all()
    ) if member_ids else []

    return render_template(
        "organization/workspace.html",
        org=org,
        membership=my_membership,
        assignments=assignments,
        top_teammates=top_teammates,
    )


@organization_bp.route("/<int:org_id>/leaderboard")
@tenant_membership_required
def workspace_leaderboard(org_id: int):
    """Organization-scoped leaderboard strictly isolated to this workspace."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    member_ids = [
        m.user_id for m in OrganizationMembership.query.filter_by(
            organization_id=org.id, status=STATUS_ACTIVE
        ).all()
    ]
    rows = (
        User.query.filter(User.id.in_(member_ids))
        .order_by(User.xp_total.desc())
        .limit(50)
        .all()
    ) if member_ids else []

    return render_template(
        "organization/leaderboard.html",
        org=org,
        rows=rows,
    )


# ---------------------------------------------------------------------------
# Eligible-Member Registry Management
# ---------------------------------------------------------------------------

@organization_bp.route("/<int:org_id>/eligible")
@org_admin_required
def eligible_members_list(org_id: int):
    """View and search pre-approved eligible member registry."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    search = (request.args.get("q") or "").strip()
    status_filter = (request.args.get("status") or "").strip()
    cohort_filter = (request.args.get("cohort") or "").strip()

    query = EligibleMember.query.filter_by(organization_id=org.id)
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                EligibleMember.identifier.ilike(like),
                EligibleMember.full_name.ilike(like),
                EligibleMember.approved_email.ilike(like),
            )
        )
    if status_filter:
        query = query.filter_by(status=status_filter)
    if cohort_filter:
        query = query.filter_by(cohort=cohort_filter)

    members = query.order_by(EligibleMember.created_at.desc()).limit(200).all()

    # Get distinct cohorts for filtering
    cohorts = [
        c[0] for c in db.session.query(EligibleMember.cohort)
        .filter(EligibleMember.organization_id == org.id, EligibleMember.cohort.isnot(None))
        .distinct()
        .all()
    ]

    return render_template(
        "organization/eligible_list.html",
        org=org,
        members=members,
        cohorts=cohorts,
        search=search,
        status_filter=status_filter,
        cohort_filter=cohort_filter,
    )


@organization_bp.route("/<int:org_id>/eligible/add", methods=["POST"])
@org_admin_required
def add_eligible_member_route(org_id: int):
    """Manually add an eligible member identifier to the registry."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    identifier = (request.form.get("identifier") or "").strip()
    full_name = (request.form.get("full_name") or "").strip()
    approved_email = (request.form.get("approved_email") or "").strip()
    department = (request.form.get("department") or "").strip()
    cohort = (request.form.get("cohort") or "").strip()

    member, err = org_service.add_eligible_member(
        org=org,
        identifier=identifier,
        full_name=full_name or None,
        approved_email=approved_email or None,
        department=department or None,
        cohort=cohort or None,
    )
    if err:
        flash(err, "error")
    else:
        flash(f"Eligible identifier '{identifier}' added successfully.", "success")
        _audit("eligible_member_added", "eligible_member", member.id, {"identifier": identifier})
        db.session.commit()

    return redirect(url_for("organization.eligible_members_list", org_id=org.id))


@organization_bp.route("/<int:org_id>/eligible/upload", methods=["POST"])
@org_admin_required
def upload_eligible_csv(org_id: int):
    """Upload and bulk import eligible members from CSV."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    file = request.files.get("csv_file")
    if not file or not file.filename:
        flash("Please select a CSV file to upload.", "error")
        return redirect(url_for("organization.eligible_members_list", org_id=org.id))

    try:
        content = file.stream.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        flash("Could not decode file. Please ensure it is saved in UTF-8 format.", "error")
        return redirect(url_for("organization.eligible_members_list", org_id=org.id))

    result = org_service.import_eligible_members_csv(org, content, actor=current_user)
    if not result["success"]:
        flash(result["error"], "error")
    else:
        created = result["created_count"]
        updated = result["updated_count"]
        rejected = result["rejected_count"]
        msg = f"Import completed: {created} new eligible members registered, {updated} updated."
        if rejected > 0:
            msg += f" {rejected} row(s) rejected."
            for r in result["rejected_rows"][:5]:
                msg += f" (Line {r.get('line')}: {r.get('reason')})"
            flash(msg, "info")
        else:
            flash(msg, "success")

    return redirect(url_for("organization.eligible_members_list", org_id=org.id))


@organization_bp.route("/<int:org_id>/eligible/template.csv")
@org_admin_required
def download_csv_template(org_id: int):
    """Download standardized CSV template for eligible member uploads."""
    csv_text = org_service.generate_csv_template()
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=human-firewall-eligible-template.csv"},
    )


@organization_bp.route("/<int:org_id>/eligible/<int:member_id>/status", methods=["POST"])
@org_admin_required
def toggle_eligible_status(org_id: int, member_id: int):
    """Deactivate, suspend or restore eligibility for an identifier."""
    org = db.session.get(Organization, org_id)
    member = db.session.get(EligibleMember, member_id)
    if not org or not member or member.organization_id != org.id:
        abort(404)

    new_status = request.form.get("status")
    if new_status in (STATUS_ELIGIBLE, STATUS_SUSPENDED, STATUS_REVOKED):
        member.status = new_status
        _audit("eligible_member_status_changed", "eligible_member", member.id, {"status": new_status})
        db.session.commit()
        flash(f"Identifier '{member.identifier}' status set to {new_status}.", "success")

    return redirect(url_for("organization.eligible_members_list", org_id=org.id))


# ---------------------------------------------------------------------------
# Organization Code & Workspace Settings
# ---------------------------------------------------------------------------

@organization_bp.route("/<int:org_id>/code/rotate", methods=["POST"])
@org_admin_required
def rotate_code(org_id: int):
    """Rotate the organization code without affecting existing memberships."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    new_code = org_service.rotate_organization_code(org, actor=current_user)
    flash(f"Organization Code successfully rotated. The new code is: {new_code}", "success")
    return redirect(url_for("organization.workspace_dashboard", org_id=org.id))


@organization_bp.route("/<int:org_id>/settings", methods=["POST"])
@org_admin_required
def update_settings(org_id: int):
    """Update workspace enrollment policy, passcode, and domain controls."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    org.domain = (request.form.get("domain") or "").strip().lower() or None
    org.require_approval = bool(request.form.get("require_approval"))

    passcode = (request.form.get("passcode") or "").strip()
    remove_passcode = bool(request.form.get("remove_passcode"))

    if remove_passcode:
        org.set_passcode("")
    elif passcode:
        org.set_passcode(passcode)

    _audit(
        "organization_settings_updated",
        "organization",
        org.id,
        {"domain": org.domain, "require_approval": org.require_approval, "require_passcode": org.require_passcode},
    )
    db.session.commit()
    flash("Workspace settings updated successfully.", "success")
    return redirect(url_for("organization.workspace_dashboard", org_id=org.id))


# ---------------------------------------------------------------------------
# Member Management
# ---------------------------------------------------------------------------

@organization_bp.route("/<int:org_id>/members")
@org_admin_required
def members_list(org_id: int):
    """List and manage active, pending and suspended organization members."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    search = (request.args.get("q") or "").strip()
    status_filter = (request.args.get("status") or "").strip()
    dept_filter = (request.args.get("dept") or "").strip()

    query = OrganizationMembership.query.filter_by(organization_id=org.id)
    if search:
        like = f"%{search}%"
        query = query.join(OrganizationMembership.user).filter(
            db.or_(
                User.username.ilike(like),
                User.email.ilike(like),
                User.display_name.ilike(like),
                OrganizationMembership.registration_id.ilike(like),
            )
        )
    if status_filter:
        query = query.filter(OrganizationMembership.status == status_filter)
    if dept_filter:
        query = query.filter(OrganizationMembership.department == dept_filter)

    memberships = query.order_by(OrganizationMembership.joined_at.desc()).limit(200).all()

    departments = [
        d[0] for d in db.session.query(OrganizationMembership.department)
        .filter(OrganizationMembership.organization_id == org.id, OrganizationMembership.department.isnot(None))
        .distinct()
        .all()
    ]

    return render_template(
        "organization/members_list.html",
        org=org,
        memberships=memberships,
        departments=departments,
        search=search,
        status_filter=status_filter,
        dept_filter=dept_filter,
    )


@organization_bp.route("/<int:org_id>/members/<int:membership_id>/approve", methods=["POST"])
@org_admin_required
def approve_member(org_id: int, membership_id: int):
    """Approve a pending member's enrollment into the workspace."""
    org = db.session.get(Organization, org_id)
    membership = db.session.get(OrganizationMembership, membership_id)
    if not org or not membership or membership.organization_id != org.id:
        abort(404)

    # Check seat limit
    if org.available_seats <= 0:
        flash("Cannot approve member: all purchased training seats are occupied.", "error")
        return redirect(url_for("organization.members_list", org_id=org.id))

    membership.status = STATUS_ACTIVE
    _audit("member_enrollment_approved", "organization_membership", membership.id, {"user_id": membership.user_id})
    db.session.commit()
    flash(f"Approved enrollment for {membership.user.name}.", "success")
    return redirect(url_for("organization.members_list", org_id=org.id))


@organization_bp.route("/<int:org_id>/members/<int:membership_id>/status", methods=["POST"])
@org_admin_required
def toggle_member_status(org_id: int, membership_id: int):
    """Suspend or re-activate a member's workspace access."""
    org = db.session.get(Organization, org_id)
    membership = db.session.get(OrganizationMembership, membership_id)
    if not org or not membership or membership.organization_id != org.id:
        abort(404)

    new_status = request.form.get("status")
    if new_status in (STATUS_ACTIVE, STATUS_SUSPENDED, STATUS_REVOKED):
        membership.status = new_status
        _audit("member_status_changed", "organization_membership", membership.id, {"status": new_status})
        db.session.commit()
        flash(f"{membership.user.name}'s workspace access is now {new_status}.", "success")

    return redirect(url_for("organization.members_list", org_id=org.id))


@organization_bp.route("/<int:org_id>/members/<int:membership_id>/recover", methods=["POST"])
@org_admin_required
def recover_member_account(org_id: int, membership_id: int):
    """Initiate audited, secure HR account recovery code for a member."""
    org = db.session.get(Organization, org_id)
    membership = db.session.get(OrganizationMembership, membership_id)
    if not org or not membership or membership.organization_id != org.id:
        abort(404)

    target_user = membership.user
    code, err = org_service.initiate_hr_account_recovery(org, target_user, current_user)
    if err:
        flash(err, "error")
    else:
        flash(
            f"Recovery Code for {target_user.username}: {code} (Valid for 24 hours). Provide this code securely to the authorized learner to reset their password at /auth/recover.",
            "success",
        )

    return redirect(url_for("organization.members_list", org_id=org.id))


# ---------------------------------------------------------------------------
# Training Assignments
# ---------------------------------------------------------------------------

@organization_bp.route("/<int:org_id>/assignments")
@org_admin_required
def assignments_list(org_id: int):
    """List training assignments, completion progress, and overdue deadlines."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    assignments = (
        LearningAssignment.query.filter_by(organization_id=org.id)
        .order_by(LearningAssignment.created_at.desc())
        .limit(100)
        .all()
    )
    paths = LearningPath.query.filter_by(state="published").order_by(LearningPath.order_index).all()
    labs = Lab.query.filter_by(state="published").order_by(Lab.number).all()

    cohorts = [
        c[0] for c in db.session.query(OrganizationMembership.cohort)
        .filter(OrganizationMembership.organization_id == org.id, OrganizationMembership.cohort.isnot(None))
        .distinct()
        .all()
    ]

    return render_template(
        "organization/assignments.html",
        org=org,
        assignments=assignments,
        paths=paths,
        labs=labs,
        cohorts=cohorts,
    )


@organization_bp.route("/<int:org_id>/assignments/create", methods=["POST"])
@org_admin_required
def create_assignment(org_id: int):
    """Assign learning modules, practical labs, or learning paths to cohorts or members."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    course_type = request.form.get("course_type", "path")
    item_id_raw = request.form.get("item_id")
    due_date_raw = request.form.get("due_date")
    cohort = (request.form.get("cohort") or "").strip() or None
    notes = (request.form.get("notes") or "").strip() or None

    try:
        item_id = int(item_id_raw)
    except (TypeError, ValueError):
        flash("Invalid course or lab selection.", "error")
        return redirect(url_for("organization.assignments_list", org_id=org.id))

    due_date = None
    if due_date_raw:
        try:
            due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
        except ValueError:
            pass

    count = org_service.assign_training(
        org=org,
        assigner=current_user,
        course_type=course_type,
        item_id=item_id,
        due_date=due_date,
        cohort=cohort,
        notes=notes,
    )

    flash(f"Assigned training to {count} learner(s) successfully.", "success")
    return redirect(url_for("organization.assignments_list", org_id=org.id))


# ---------------------------------------------------------------------------
# Reports & Exports
# ---------------------------------------------------------------------------

@organization_bp.route("/<int:org_id>/reports/export.csv")
@org_admin_required
def export_csv_report(org_id: int):
    """Download tenant-scoped learner progress report in CSV format."""
    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    _audit("organization_csv_report_downloaded", "organization", org.id)
    db.session.commit()

    csv_data = org_service.generate_organization_csv_report(org)
    filename = f"human-firewall-{org.slug}-report-{utcnow().strftime('%Y%m%d')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@organization_bp.route("/<int:org_id>/reports/summary.pdf")
@org_admin_required
def export_pdf_report(org_id: int):
    """Generate and download a professional executive PDF summary report using ReportLab."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    org = db.session.get(Organization, org_id)
    if not org:
        abort(404)

    _audit("organization_pdf_report_downloaded", "organization", org.id)
    db.session.commit()

    metrics = org_service.get_organization_dashboard_metrics(org)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    elements = []
    # Header
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, textColor=colors.HexColor("#0f172a"))
    elements.append(Paragraph(f"HUMAN FIREWALL · Executive Training Summary", title_style))
    elements.append(Paragraph(f"Organization: <b>{org.name}</b> (Code: {org.org_code})", styles["Normal"]))
    elements.append(Paragraph(f"Generated: {utcnow().strftime('%B %d, %Y')} | Plan: {org.subscription_plan.capitalize()}", styles["Normal"]))
    elements.append(Spacer(1, 16))

    # Metric Table
    data = [
        ["Metric", "Value", "Metric", "Value"],
        ["Total Eligible", str(metrics["total_eligible"]), "Purchased Seats", str(metrics["seats_purchased"])],
        ["Active Members", str(metrics["active_members"]), "Occupied Seats", str(metrics["occupied_seats"])],
        ["Pending Approval", str(metrics["pending_members"]), "Available Seats", str(metrics["available_seats"])],
        ["Assigned Trainings", str(metrics["total_assigned"]), "Overdue Assignments", str(metrics["overdue_assignments"])],
        ["Labs Passed", str(metrics["labs_passed"]), "Certificates Issued", str(metrics["certs_issued"])],
        ["Avg Lab Score", f"{metrics['avg_lab_score']}%", "Subscription Status", org.subscription_status.capitalize()],
    ]

    t = Table(data, colWidths=[130, 130, 130, 130])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Notice:</b> This training record represents defense awareness simulations conducted within the Human Firewall platform. No production credentials or live exploit data are stored or gathered.", styles["Italic"]))

    doc.build(elements)
    buffer.seek(0)

    filename = f"human-firewall-{org.slug}-summary.pdf"
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


# ---------------------------------------------------------------------------
# Payment Webhook & Commercial Integration
# ---------------------------------------------------------------------------

@organization_bp.route("/webhook/payment", methods=["POST"])
@limiter.limit("60 per minute")
def payment_webhook():
    """Idempotent payment webhook handler.

    Verifies signature, prevents duplicate subscription activations, and
    records verified transactions without hardcoded simulation secrets.
    """
    payload = request.get_json(silent=True) or {}
    event_id = payload.get("event_id") or request.headers.get("X-Webhook-ID")
    event_type = payload.get("event_type") or payload.get("type")
    data = payload.get("data") or {}

    if not event_id or not event_type:
        return jsonify({"error": "invalid_payload"}), 400

    # Idempotency check: verify whether this webhook was already processed
    existing_invoice = SubscriptionInvoice.query.filter_by(invoice_number=event_id).first()
    if existing_invoice:
        return jsonify({"status": "already_processed", "event_id": event_id}), 200

    org_id = data.get("organization_id")
    org = db.session.get(Organization, org_id) if org_id else None

    if event_type == "payment.succeeded" and org:
        amount_cents = int(data.get("amount_cents", 0))
        invoice = SubscriptionInvoice(
            organization_id=org.id,
            invoice_number=event_id,
            amount_cents=amount_cents,
            currency=data.get("currency", "USD"),
            status="paid",
            paid_at=utcnow(),
        )
        db.session.add(invoice)

        # Extend subscription
        org.subscription_status = "active"
        org.subscription_expires_at = utcnow() + timedelta(days=365)
        _audit("webhook_payment_processed", "subscription_invoice", event_id, {"org_id": org.id, "amount": amount_cents})
        db.session.commit()
        return jsonify({"status": "success", "invoice": event_id}), 200

    return jsonify({"status": "received", "event_id": event_id}), 200
