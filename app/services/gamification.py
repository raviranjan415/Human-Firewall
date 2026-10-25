"""Gamification engine: XP ledger, streaks, achievements and leaderboards."""

from __future__ import annotations

import math
from datetime import date, datetime, timedelta

from flask import current_app
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import (
    Achievement,
    Certificate,
    LabAttempt,
    LearningEvent,
    StreakDay,
    User,
    UserAchievement,
    XPTransaction,
)
from app.models.user import utcnow


# ---------------------------------------------------------------------------
# Levels
# ---------------------------------------------------------------------------

def level_for_xp(xp: int) -> int:
    """Transparent level curve: level 2 at 100 XP, 3 at 400, 4 at 900, ..."""
    xp = max(0, int(xp or 0))
    return 1 + int(math.isqrt(xp // 100))


def xp_for_level(level: int) -> int:
    """Minimum XP required to reach ``level``."""
    return max(0, (max(1, level) - 1) ** 2 * 100)


def level_progress(xp: int) -> dict:
    level = level_for_xp(xp)
    floor = xp_for_level(level)
    ceiling = xp_for_level(level + 1)
    span = max(1, ceiling - floor)
    return {
        "level": level,
        "current_xp": xp,
        "level_floor": floor,
        "next_level_xp": ceiling,
        "percent": int(min(100, max(0, (xp - floor) / span * 100))),
    }


# ---------------------------------------------------------------------------
# XP ledger
# ---------------------------------------------------------------------------

def award_xp(
    user: User,
    amount: int,
    reason: str,
    reference_type: str = "",
    reference_id: str = "",
    note: str | None = None,
) -> int:
    """Award XP exactly once for a qualifying event.

    The ``XPTransaction`` unique constraint makes replays idempotent: replaying
    a completed activity never pays out again.

    Returns the amount actually credited (0 when it was a duplicate).
    """
    amount = int(amount or 0)
    if amount <= 0 or user is None:
        return 0

    transaction = XPTransaction(
        user_id=user.id,
        amount=amount,
        reason=reason,
        reference_type=str(reference_type or ""),
        reference_id=str(reference_id or ""),
        note=note,
    )
    # Insert inside a savepoint: a duplicate must only discard this one ledger
    # row, never roll back the caller's pending work (progress, streak, ...).
    try:
        with db.session.begin_nested():
            db.session.add(transaction)
            db.session.flush()
    except IntegrityError:
        return 0

    user.xp_total = (user.xp_total or 0) + amount
    user.level = level_for_xp(user.xp_total)
    log_event(user.id, "xp_awarded", item_type=reference_type or None,
              score=amount, payload={"reason": reason, "reference": reference_id})
    return amount


def xp_breakdown(user_id: int) -> list[dict]:
    rows = (
        db.session.query(XPTransaction.reason, func.sum(XPTransaction.amount))
        .filter(XPTransaction.user_id == user_id)
        .group_by(XPTransaction.reason)
        .all()
    )
    return [{"reason": reason, "xp": int(total or 0)} for reason, total in rows]


def xp_reward_for(level: str) -> int:
    rewards = current_app.config.get("XP_REWARDS", {})
    key = current_app.config.get("LAB_LEVEL_XP", {}).get(level, "lab_basic")
    return int(rewards.get(key, 30))


# ---------------------------------------------------------------------------
# Streaks
# ---------------------------------------------------------------------------

def record_streak_activity(user: User, day: date | None = None, xp_earned: int = 0) -> StreakDay:
    """Count a streak day only after a qualifying learning activity."""
    day = day or date.today()
    record = StreakDay.query.filter_by(user_id=user.id, day=day).first()
    if record is None:
        record = StreakDay(user_id=user.id, day=day, qualified=True, activity_count=1,
                           xp_earned=xp_earned)
        db.session.add(record)
    else:
        record.qualified = True
        record.activity_count = (record.activity_count or 0) + 1
        record.xp_earned = (record.xp_earned or 0) + xp_earned

    user.last_activity_date = day
    _recalculate_streak_counters(user, day)
    return record


def _recalculate_streak_counters(user: User, today: date) -> None:
    days = {
        row.day
        for row in StreakDay.query.filter_by(user_id=user.id, qualified=True)
        .filter(StreakDay.day <= today)
        .all()
    }
    if not days:
        user.current_streak = 0
        return

    # Current streak counts back from today (or yesterday, so a learner who has
    # not yet studied today does not lose their streak instantly).
    anchor = today if today in days else today - timedelta(days=1)
    current = 0
    cursor = anchor
    while cursor in days:
        current += 1
        cursor -= timedelta(days=1)

    user.current_streak = current
    user.longest_streak = max(user.longest_streak or 0, current, len(days) and _longest_run(days))


def _longest_run(days: set[date]) -> int:
    ordered = sorted(days)
    longest = run = 1
    for previous, current in zip(ordered, ordered[1:]):
        if (current - previous).days == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1
    return longest if ordered else 0


# ---------------------------------------------------------------------------
# Analytics events
# ---------------------------------------------------------------------------

def log_event(
    user_id: int,
    event_type: str,
    item_type: str | None = None,
    item_id: int | None = None,
    duration_seconds: int = 0,
    success: bool | None = None,
    score: int | None = None,
    payload: dict | None = None,
) -> LearningEvent:
    import json

    event = LearningEvent(
        user_id=user_id,
        event_type=event_type,
        item_type=item_type,
        item_id=item_id,
        duration_seconds=int(duration_seconds or 0),
        success=success,
        score=score,
        payload_json=json.dumps(payload) if payload else None,
    )
    db.session.add(event)
    return event


# ---------------------------------------------------------------------------
# Achievements
# ---------------------------------------------------------------------------

def user_stats(user: User) -> dict:
    """Derived statistics used by achievement rules and the dashboard."""
    from app.models import UserProgress

    completed_labs = (
        db.session.query(func.count(func.distinct(LabAttempt.lab_id)))
        .filter(LabAttempt.user_id == user.id, LabAttempt.passed.is_(True))
        .scalar()
        or 0
    )
    perfect = (
        db.session.query(func.count(LabAttempt.id))
        .filter(LabAttempt.user_id == user.id, LabAttempt.percentage >= 100)
        .scalar()
        or 0
    )
    no_hint_labs = (
        db.session.query(func.count(func.distinct(LabAttempt.lab_id)))
        .filter(
            LabAttempt.user_id == user.id,
            LabAttempt.passed.is_(True),
            LabAttempt.hints_used == 0,
        )
        .scalar()
        or 0
    )
    by_type = dict(
        db.session.query(UserProgress.item_type, func.count(UserProgress.id))
        .filter(UserProgress.user_id == user.id, UserProgress.status == "completed")
        .group_by(UserProgress.item_type)
        .all()
    )
    certificates = (
        db.session.query(func.count(Certificate.id))
        .filter(Certificate.user_id == user.id, Certificate.revoked.is_(False))
        .scalar()
        or 0
    )
    return {
        "labs_completed": int(completed_labs),
        "perfect_scores": int(perfect),
        "no_hint_labs": int(no_hint_labs),
        "videos_completed": int(by_type.get("video", 0)),
        "comics_completed": int(by_type.get("comic", 0)),
        "games_completed": int(by_type.get("game", 0)),
        "certificates": int(certificates),
        "streak": int(user.current_streak or 0),
        "longest_streak": int(user.longest_streak or 0),
        "xp": int(user.xp_total or 0),
        "level": level_for_xp(user.xp_total or 0),
    }


def _criteria_met(achievement: Achievement, stats: dict) -> bool:
    kind = achievement.criteria_type
    value = int(achievement.criteria_value or 0)
    if kind == "labs_completed":
        return stats["labs_completed"] >= value
    if kind == "perfect_score":
        return stats["perfect_scores"] >= max(1, value)
    if kind == "no_hint_labs":
        return stats["no_hint_labs"] >= max(1, value)
    if kind == "streak":
        return max(stats["streak"], stats["longest_streak"]) >= value
    if kind == "videos_completed":
        return stats["videos_completed"] >= value
    if kind == "comics_completed":
        return stats["comics_completed"] >= value
    if kind == "games_completed":
        return stats["games_completed"] >= value
    if kind == "level":
        return stats["level"] >= value
    if kind == "certificate_tier":
        return (
            Certificate.query.filter_by(user_id=stats["user_id"], tier=achievement.criteria_extra)
            .filter(Certificate.revoked.is_(False))
            .first()
            is not None
        )
    return False


def evaluate_achievements(user: User) -> list[Achievement]:
    """Award any achievements whose criteria the learner now satisfies."""
    stats = user_stats(user)
    stats["user_id"] = user.id
    existing = {
        row.achievement_id
        for row in UserAchievement.query.filter_by(user_id=user.id).all()
    }
    newly_awarded: list[Achievement] = []
    for achievement in Achievement.query.filter_by(is_active=True).all():
        if achievement.id in existing:
            continue
        if _criteria_met(achievement, stats):
            db.session.add(UserAchievement(user_id=user.id, achievement_id=achievement.id))
            newly_awarded.append(achievement)
            if achievement.xp_bonus:
                award_xp(
                    user,
                    achievement.xp_bonus,
                    reason="achievement",
                    reference_type="achievement",
                    reference_id=achievement.code,
                )
    return newly_awarded


# ---------------------------------------------------------------------------
# Leaderboards
# ---------------------------------------------------------------------------

VALID_SCOPES = ("global", "weekly", "monthly", "beginner")


def leaderboard(scope: str = "global", limit: int = 20) -> list[dict]:
    """Server-computed ranking. Only display names are exposed."""
    query = db.session.query(
        User.id,
        func.coalesce(User.display_name, User.username).label("name"),
        User.xp_total,
        User.level,
    ).filter(User.is_active.is_(True))

    if scope in ("weekly", "monthly"):
        days = 7 if scope == "weekly" else 30
        since = utcnow() - timedelta(days=days)
        gained = (
            db.session.query(
                XPTransaction.user_id.label("uid"),
                func.sum(XPTransaction.amount).label("gained"),
            )
            .filter(XPTransaction.created_at >= since)
            .group_by(XPTransaction.user_id)
            .subquery()
        )
        query = db.session.query(
            User.id,
            func.coalesce(User.display_name, User.username).label("name"),
            func.coalesce(gained.c.gained, 0).label("window_xp"),
            User.level,
        ).outerjoin(gained, gained.c.uid == User.id).filter(User.is_active.is_(True))
        rows = query.order_by(func.coalesce(gained.c.gained, 0).desc()).limit(limit).all()
        return [
            {"rank": i, "user_id": r.id, "name": r.name, "xp": int(r.window_xp or 0), "level": r.level}
            for i, r in enumerate(rows, start=1)
        ]

    if scope == "beginner":
        query = query.filter(User.xp_total < 500)

    rows = query.order_by(User.xp_total.desc(), User.id.asc()).limit(limit).all()
    return [
        {"rank": i, "user_id": r.id, "name": r.name, "xp": int(r.xp_total or 0), "level": r.level}
        for i, r in enumerate(rows, start=1)
    ]


def user_rank(user: User) -> int | None:
    if not user or not user.is_active:
        return None
    higher = User.query.filter(
        User.is_active.is_(True), User.xp_total > (user.xp_total or 0)
    ).count()
    return higher + 1
