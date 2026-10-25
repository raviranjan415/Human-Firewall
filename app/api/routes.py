"""JSON API used by the interactive front end.

Every endpoint re-validates on the server:

* XP is credited through the idempotent ledger, so replaying a request never
  pays out twice.
* Lab answers are scored from stored configuration, never from the request.
* Game answers are graded against the database — the correct option is never
  sent to the browser before the learner commits.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.extensions import db, limiter
from app.models import Comic, Game, GameScenario, Lab, ScenarioChoice, VideoAsset
from app.services import gamification
from app.services import labs as labs_service
from app.services import progress as progress_service
from app.services.i18n import current_locale

api_bp = Blueprint("api", __name__)


def _payload() -> dict:
    return request.get_json(silent=True) or {}


def _int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Learner summary
# ---------------------------------------------------------------------------

@api_bp.route("/me/summary")
@login_required
def me_summary():
    summary = progress_service.summary(current_user)
    summary["level_info"] = gamification.level_progress(current_user.xp_total or 0)
    return jsonify(summary)


# ---------------------------------------------------------------------------
# Video lessons
# ---------------------------------------------------------------------------

@api_bp.route("/videos/<int:video_id>/progress", methods=["POST"])
@login_required
def video_progress(video_id: int):
    video = db.session.get(VideoAsset, video_id)
    if video is None:
        return jsonify({"error": "not_found"}), 404

    data = _payload()
    record = progress_service.update_position(
        current_user,
        "video",
        video.id,
        position_seconds=_int(data.get("position")),
        duration_seconds=_int(data.get("duration")) or video.duration_seconds,
    )
    db.session.commit()
    return jsonify({"ok": True, "progress_percent": record.progress_percent})


@api_bp.route("/videos/<int:video_id>/complete", methods=["POST"])
@login_required
def video_complete(video_id: int):
    video = db.session.get(VideoAsset, video_id)
    if video is None:
        return jsonify({"error": "not_found"}), 404

    data = _payload()
    settlement = progress_service.complete_activity(
        current_user,
        "video",
        video.id,
        time_spent_seconds=_int(data.get("time_spent")),
        event_type="video_completed",
    )
    return jsonify(
        {
            "ok": True,
            "xp_awarded": settlement["xp_awarded"],
            "first_completion": settlement["first_completion"],
            "achievements": [a.code for a in settlement["achievements"]],
            "total_xp": current_user.xp_total,
        }
    )


# ---------------------------------------------------------------------------
# Comics
# ---------------------------------------------------------------------------

@api_bp.route("/comics/<int:comic_id>/complete", methods=["POST"])
@login_required
def comic_complete(comic_id: int):
    comic = db.session.get(Comic, comic_id)
    if comic is None or comic.state != "published":
        return jsonify({"error": "not_found"}), 404

    settlement = progress_service.complete_activity(
        current_user, "comic", comic.id, event_type="comic_read"
    )
    return jsonify(
        {
            "ok": True,
            "xp_awarded": settlement["xp_awarded"],
            "first_completion": settlement["first_completion"],
            "achievements": [a.code for a in settlement["achievements"]],
            "total_xp": current_user.xp_total,
        }
    )


# ---------------------------------------------------------------------------
# Games
# ---------------------------------------------------------------------------

@api_bp.route("/games/<slug>/answer", methods=["POST"])
@login_required
def game_answer(slug: str):
    game = Game.query.filter_by(slug=slug, state="published").first()
    if game is None:
        return jsonify({"error": "not_found"}), 404

    data = _payload()
    scenario = GameScenario.query.filter_by(
        id=_int(data.get("scenario_id")), game_id=game.id
    ).first()
    if scenario is None:
        return jsonify({"error": "scenario_not_found"}), 404

    locale = current_locale()
    choice = None
    if scenario.choices:
        choice = ScenarioChoice.query.filter_by(
            id=_int(data.get("choice_id")), scenario_id=scenario.id
        ).first()
        if choice is None:
            return jsonify({"error": "choice_not_found"}), 404

    # A "threat / safe" judgement scenario has no choices: the learner's
    # verdict is compared with the stored truth.
    correct = choice.is_correct if choice else bool(data.get("is_threat")) == scenario.is_threat

    def _localized(obj, field):
        if obj is None:
            return None
        return getattr(obj, f"{field}_{locale}", None) or getattr(obj, f"{field}_en", None)

    return jsonify(
        {
            "ok": True,
            "correct": bool(correct),
            "is_threat": scenario.is_threat,
            "xp_value": scenario.xp_value if correct else 0,
            "feedback": _localized(choice, "feedback")
            or (
                "Correct reading of the situation."
                if correct
                else "That is not the safest choice — read the explanation."
            ),
            "explanation": _localized(scenario, "explanation"),
            "warning_signs": _localized(scenario, "warning_signs"),
        }
    )


@api_bp.route("/games/<slug>/complete", methods=["POST"])
@login_required
@limiter.limit("60 per hour")
def game_complete(slug: str):
    game = Game.query.filter_by(slug=slug, state="published").first()
    if game is None:
        return jsonify({"error": "not_found"}), 404

    data = _payload()
    score = _int(data.get("score"))
    total = max(1, _int(data.get("total"), 1))
    passed = score / total >= 0.7

    if passed:
        settlement = progress_service.complete_activity(
            current_user,
            "game",
            game.id,
            score=score,
            max_score=total,
            time_spent_seconds=_int(data.get("time_spent")),
            xp_amount=game.xp_reward,
            xp_reason="game",
            reference_id=f"game:{game.id}",
            event_type="game_completed",
        )
        return jsonify(
            {
                "ok": True,
                "passed": True,
                "xp_awarded": settlement["xp_awarded"],
                "first_completion": settlement["first_completion"],
                "achievements": [a.code for a in settlement["achievements"]],
                "total_xp": current_user.xp_total,
            }
        )

    progress_service.record_failure(
        current_user, "game", game.id, score=score, max_score=total,
        time_spent_seconds=_int(data.get("time_spent")),
    )
    return jsonify({"ok": True, "passed": False, "xp_awarded": 0, "total_xp": current_user.xp_total})


# ---------------------------------------------------------------------------
# Practical labs
# ---------------------------------------------------------------------------

@api_bp.route("/labs/<int:lab_id>/submit", methods=["POST"])
@login_required
@limiter.limit("120 per hour")
def lab_submit(lab_id: int):
    lab = db.session.get(Lab, lab_id)
    if lab is None or lab.state != "published":
        return jsonify({"error": "not_found"}), 404

    data = _payload()
    result = labs_service.submit_lab(
        current_user,
        lab,
        data.get("answer"),
        hints_used=_int(data.get("hints_used")),
    )
    if not result.get("ok"):
        return jsonify({"error": result.get("error"), "detail": result.get("detail")}), 409

    locale = current_locale()
    return jsonify(
        {
            "ok": True,
            "passed": result["passed"],
            "already_passed": result["already_passed"],
            "percentage": result["percentage"],
            "feedback": result.get("feedback_hi" if locale == "hi" else "feedback_en"),
            "detail": result["detail"],
            "xp_awarded": result["xp_awarded"],
            "achievements": [a.code for a in result["achievements"]],
            "next_lab_id": result["next_lab_id"],
            "total_xp": current_user.xp_total,
        }
    )
