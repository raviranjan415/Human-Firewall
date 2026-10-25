"""Progress tracking service.

Every completion funnels through :func:`complete_activity`, which:
  1. updates the ``UserProgress`` row,
  2. credits XP exactly once (idempotent ledger),
  3. records the streak day, and
  4. re-evaluates achievements.
"""

from __future__ import annotations

from datetime import datetime

from flask import current_app

from app.extensions import db
from app.models import User, UserProgress
from app.models.user import utcnow
from app.services import gamification

XP_REASON_BY_TYPE = {
    "video": "video_lesson",
    "comic": "comic",
    "game": "game",
    "lab": "lab",
    "lesson": "video_lesson",
    "challenge": "daily_challenge",
}


def get_progress(user_id: int, item_type: str, item_id: int) -> UserProgress | None:
    return UserProgress.query.filter_by(
        user_id=user_id, item_type=item_type, item_id=item_id
    ).first()


def get_or_create_progress(user_id: int, item_type: str, item_id: int) -> UserProgress:
    record = get_progress(user_id, item_type, item_id)
    if record is None:
        record = UserProgress(user_id=user_id, item_type=item_type, item_id=item_id)
        db.session.add(record)
        db.session.flush()
    return record


def start_activity(user: User, item_type: str, item_id: int) -> UserProgress:
    record = get_or_create_progress(user.id, item_type, item_id)
    if record.status == "not_started":
        record.status = "in_progress"
        gamification.log_event(user.id, "activity_started", item_type, item_id)
    return record


def update_position(user: User, item_type: str, item_id: int, position_seconds: int,
                    duration_seconds: int | None = None) -> UserProgress:
    """Remember video playback position so learners can resume."""
    record = get_or_create_progress(user.id, item_type, item_id)
    record.last_position_seconds = max(0, int(position_seconds or 0))
    if record.status == "not_started":
        record.status = "in_progress"
    if duration_seconds:
        record.progress_percent = int(
            min(99, record.last_position_seconds / max(1, duration_seconds) * 100)
        )
    return record


def complete_activity(
    user: User,
    item_type: str,
    item_id: int,
    score: int | None = None,
    max_score: int = 100,
    time_spent_seconds: int = 0,
    hints_used: int = 0,
    xp_amount: int | None = None,
    xp_reason: str | None = None,
    reference_id: str | None = None,
    event_type: str = "activity_completed",
) -> dict:
    """Mark an activity complete and settle XP, streak and achievements."""
    record = get_or_create_progress(user.id, item_type, item_id)
    was_completed = record.status == "completed"

    record.status = "completed"
    record.progress_percent = 100
    if score is not None:
        record.best_score = max(record.best_score or 0, int(score))
    if record.first_attempt_passed is None:
        record.first_attempt_passed = True
    record.attempts_count = (record.attempts_count or 0) + 1
    record.hints_used = max(record.hints_used or 0, int(hints_used or 0))
    record.time_spent_seconds = (record.time_spent_seconds or 0) + int(time_spent_seconds or 0)
    if record.completed_at is None:
        record.completed_at = utcnow()

    reason = xp_reason or XP_REASON_BY_TYPE.get(item_type, "activity")
    if xp_amount is None:
        rewards = current_app.config.get("XP_REWARDS", {})
        xp_amount = int(rewards.get(reason, 0))

    perfect_bonus = 0
    if score is not None and max_score and int(score) >= int(max_score):
        perfect_bonus = int(current_app.config.get("XP_REWARDS", {}).get("perfect_bonus", 0))

    reference = reference_id if reference_id is not None else f"{item_type}:{item_id}"

    earned = gamification.award_xp(
        user, xp_amount or 0, reason=reason, reference_type=item_type, reference_id=reference
    )
    bonus = gamification.award_xp(
        user, perfect_bonus, reason="perfect_bonus",
        reference_type=item_type, reference_id=reference,
    )

    gamification.record_streak_activity(user, xp_earned=earned + bonus)
    gamification.log_event(
        user.id, event_type, item_type, item_id,
        duration_seconds=time_spent_seconds, success=True, score=score,
    )
    new_achievements = gamification.evaluate_achievements(user)

    db.session.commit()
    return {
        "xp_awarded": earned + bonus,
        "first_completion": not was_completed,
        "achievements": new_achievements,
        "progress": record,
    }


def record_failure(
    user: User,
    item_type: str,
    item_id: int,
    score: int = 0,
    max_score: int = 100,
    hints_used: int = 0,
    time_spent_seconds: int = 0,
) -> UserProgress:
    """Track an unsuccessful attempt without awarding XP.

    A wrong decision is a learning opportunity: nothing is taken away and the
    activity stays replayable.
    """
    record = get_or_create_progress(user.id, item_type, item_id)
    record.status = "in_progress" if record.status != "completed" else "completed"
    record.attempts_count = (record.attempts_count or 0) + 1
    record.best_score = max(record.best_score or 0, int(score or 0))
    record.hints_used = max(record.hints_used or 0, int(hints_used or 0))
    record.time_spent_seconds = (record.time_spent_seconds or 0) + int(time_spent_seconds or 0)
    if record.first_attempt_passed is None:
        record.first_attempt_passed = False
    record.progress_percent = int(min(99, max(record.progress_percent or 0, 25)))
    gamification.log_event(
        user.id, "activity_failed", item_type, item_id,
        duration_seconds=time_spent_seconds, success=False, score=score,
    )
    db.session.commit()
    return record


def summary(user: User) -> dict:
    """Aggregate progress counters for the dashboard and analytics pages."""
    stats = gamification.user_stats(user)
    total_labs = 100
    stats.update(
        {
            "total_labs": total_labs,
            "labs_percent": int(stats["labs_completed"] / total_labs * 100),
            "completion_percent": int(
                min(
                    100,
                    (
                        stats["labs_completed"]
                        + stats["videos_completed"]
                        + stats["comics_completed"]
                    )
                    / 250
                    * 100,
                )
            ),
            "rank": gamification.user_rank(user),
            "level_info": gamification.level_progress(user.xp_total or 0),
            "last_activity": user.last_activity_date,
        }
    )
    return stats


def next_certificate_milestone(labs_completed: int) -> dict | None:
    """Return the next certificate tier and how far away it is."""
    tiers = [("basic", 30), ("intermediate", 60), ("advanced", 90), ("master", 100)]
    for tier, required in tiers:
        if labs_completed < required:
            return {
                "tier": tier,
                "required": required,
                "remaining": required - labs_completed,
                "percent": int(labs_completed / required * 100),
            }
    return None
