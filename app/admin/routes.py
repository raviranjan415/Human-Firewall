"""Administrator console: platform overview, users, content workflow and audit.

Every privileged action is written to the append-only ``AuditLog``. Passwords,
session tokens and other secrets are never recorded.
"""

from __future__ import annotations

import json

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.auth.decorators import admin_required
from app.extensions import db
from app.models import (
    AuditLog,
    Comic,
    CyberNews,
    Game,
    HistoricalIncident,
    Lab,
    User,
    VideoAsset,
)
from app.models.content import CONTENT_STATES
from app.models.user import ROLES
from app.services import analytics

admin_bp = Blueprint("admin", __name__)


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


@admin_bp.route("/")
@admin_required
def index():
    return render_template(
        "admin/index.html",
        overview=analytics.admin_overview(),
        hardest=analytics.hardest_labs(),
        recent_audit=AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all(),
        content_states={
            "labs_published": Lab.query.filter_by(state="published").count(),
            "labs_draft": Lab.query.filter_by(state="draft").count(),
            "labs_total": Lab.query.count(),
            "comics": Comic.query.count(),
            "games": Game.query.count(),
            "videos": VideoAsset.query.count(),
            "incidents": HistoricalIncident.query.count(),
        },
    )


@admin_bp.route("/users")
@admin_required
def users():
    search = (request.args.get("q") or "").strip()
    role_name = (request.args.get("role") or "").strip()

    query = User.query
    if search:
        like = f"%{search}%"
        query = query.filter(db.or_(User.username.ilike(like), User.email.ilike(like)))
    if role_name in ROLES:
        query = query.join(User.role).filter_by(name=role_name)

    return render_template(
        "admin/users.html",
        users=query.order_by(User.created_at.desc()).limit(200).all(),
        roles=ROLES,
        selected={"q": search, "role": role_name},
    )


@admin_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@admin_required
def toggle_user(user_id: int):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "error")
        return redirect(url_for("admin.users"))

    user.is_active = not user.is_active
    _audit("user_active_toggled", "user", user.id, {"is_active": user.is_active})
    db.session.commit()
    flash(f"{user.name} is now {'active' if user.is_active else 'disabled'}.", "success")
    return redirect(url_for("admin.users", q=request.args.get("q"), role=request.args.get("role")))


@admin_bp.route("/content")
@admin_required
def content():
    state = (request.args.get("state") or "").strip()
    query = Lab.query
    if state in CONTENT_STATES:
        query = query.filter_by(state=state)
    return render_template(
        "admin/content.html",
        labs=query.order_by(Lab.number).limit(120).all(),
        states=CONTENT_STATES,
        selected_state=state,
        counts={s: Lab.query.filter_by(state=s).count() for s in CONTENT_STATES},
    )


@admin_bp.route("/content/labs/<int:lab_id>/state", methods=["POST"])
@admin_required
def set_lab_state(lab_id: int):
    lab = db.session.get(Lab, lab_id)
    if lab is None:
        abort(404)
    new_state = (request.form.get("state") or "").strip()
    if new_state not in CONTENT_STATES:
        abort(400)

    # A lab without authored tasks must never be published by accident.
    if new_state == "published" and not lab.task_en:
        flash(
            f"Lab {lab.number} has no authored task yet — it cannot be published.",
            "error",
        )
        return redirect(url_for("admin.content", state=request.args.get("state")))

    previous, lab.state = lab.state, new_state
    _audit("lab_state_changed", "lab", lab.id, {"from": previous, "to": new_state})
    db.session.commit()
    flash(f"Lab {lab.number} moved from {previous} to {new_state}.", "success")
    return redirect(url_for("admin.content", state=request.args.get("state")))


@admin_bp.route("/news")
@admin_required
def news_queue():
    state = (request.args.get("state") or "pending").strip()
    query = CyberNews.query
    if state in ("pending", "approved", "rejected"):
        query = query.filter_by(review_state=state)
    return render_template(
        "admin/news.html",
        stories=query.order_by(CyberNews.fetched_at.desc()).limit(100).all(),
        selected_state=state,
        counts={
            s: CyberNews.query.filter_by(review_state=s).count()
            for s in ("pending", "approved", "rejected")
        },
    )


@admin_bp.route("/news/<int:news_id>/review", methods=["POST"])
@admin_required
def review_news(news_id: int):
    story = db.session.get(CyberNews, news_id)
    if story is None:
        abort(404)
    decision = (request.form.get("decision") or "").strip()
    if decision not in ("approved", "rejected"):
        abort(400)

    story.review_state = decision
    story.reviewed_by_id = current_user.id
    _audit("news_reviewed", "cyber_news", story.id, {"decision": decision})
    db.session.commit()
    flash(f"Story marked {decision}.", "success")
    return redirect(url_for("admin.news_queue", state=request.args.get("state", "pending")))


@admin_bp.route("/audit")
@admin_required
def audit():
    return render_template(
        "admin/audit.html",
        entries=AuditLog.query.order_by(AuditLog.created_at.desc()).limit(200).all(),
    )
