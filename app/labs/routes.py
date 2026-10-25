"""Practical lab pages: the quest map and one lab at a time.

Answers are never trusted from the browser. ``app.api`` re-scores every
submission against the lab's stored validation configuration and refuses to
accept a lab whose prerequisites are not met.
"""

from __future__ import annotations

import json

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Lab
from app.services import labs as labs_service
from app.services import progress as progress_service
from app.services.i18n import current_locale

labs_bp = Blueprint("labs", __name__)


def _localized_list(raw: str | None) -> list:
    """Resolve a bilingual JSON list (options or hints) into the active locale."""
    try:
        data = json.loads(raw or "[]")
    except ValueError:
        return []
    if not isinstance(data, list):
        return []
    locale = current_locale()
    resolved = []
    for item in data:
        if isinstance(item, dict):
            if "en" in item or "hi" in item:
                resolved.append({"id": item.get("id"), "text": item.get(locale) or item.get("en") or ""})
            else:
                resolved.append(item)
        else:
            resolved.append({"id": None, "text": str(item)})
    return resolved


def _payload(raw: str | None):
    try:
        return json.loads(raw or "null")
    except ValueError:
        return None


@labs_bp.route("/")
@login_required
def index():
    level = (request.args.get("level") or "").strip()
    path = labs_service.lab_path(current_user)
    if level:
        path = [row for row in path if row["lab"].level == level]
    return render_template(
        "labs/index.html",
        path=path,
        levels=labs_service.level_summary(current_user),
        total_labs=Lab.query.filter_by(state="published").count(),
        completed_labs=len(labs_service.passed_lab_ids(current_user)),
        selected_level=level,
    )


@labs_bp.route("/<int:lab_id>")
@login_required
def detail(lab_id: int):
    lab = db.session.get(Lab, lab_id)
    if lab is None or lab.state != "published":
        abort(404)

    status = labs_service.unlock_status(current_user, lab)
    if not status["unlocked"]:
        prerequisite = (
            db.session.get(Lab, status.get("prerequisite_id"))
            if status.get("prerequisite_id")
            else None
        )
        return render_template(
            "labs/locked.html",
            lab=lab,
            lock=status,
            prerequisite=prerequisite,
        )

    progress_service.start_activity(current_user, "lab", lab.id)
    db.session.commit()

    best = labs_service.best_attempt(current_user, lab.id)
    next_lab = (
        Lab.query.filter(Lab.number > lab.number, Lab.state == "published")
        .order_by(Lab.number)
        .first()
    )
    return render_template(
        "labs/detail.html",
        lab=lab,
        best=best,
        attempts=labs_service.attempts_for(current_user, lab.id),
        options=_localized_list(lab.options_json),
        hints=_localized_list(lab.hints_json),
        payload=_payload(lab.payload_json),
        next_lab=next_lab,
        xp_reward=lab.xp_reward,
        passed=lab.id in labs_service.passed_lab_ids(current_user),
    )


@labs_bp.route("/next")
@login_required
def next_lab():
    """Send the learner to the next unlocked, unpassed lab."""
    ready = labs_service.recommendations(current_user, limit=1)
    if ready:
        return redirect(url_for("labs.detail", lab_id=ready[0].id))
    return redirect(url_for("labs.index"))
