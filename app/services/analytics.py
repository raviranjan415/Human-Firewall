"""Analytics service — real aggregates computed from recorded activity."""

from __future__ import annotations

import csv
import io
from collections import defaultdict
from datetime import date, timedelta

from sqlalchemy import func

from app.extensions import db
from app.models import (
    Achievement,
    AssessmentAttempt,
    Certificate,
    Comic,
    CyberNews,
    Lab,
    LabAttempt,
    LearningEvent,
    User,
    UserAchievement,
    UserProgress,
    VideoAsset,
)
from app.models.user import ROLE_LEARNER, utcnow
from app.services import gamification


# ---------------------------------------------------------------------------
# Learner analytics
# ---------------------------------------------------------------------------

def weekly_activity(user_id: int, days: int = 7) -> dict:
    start = date.today() - timedelta(days=days - 1)
    rows = (
        db.session.query(func.date(LearningEvent.created_at), func.count(LearningEvent.id))
        .filter(LearningEvent.user_id == user_id, LearningEvent.created_at >= start)
        .group_by(func.date(LearningEvent.created_at))
        .all()
    )
    counts = {str(day): count for day, count in rows}
    labels, values = [], []
    for offset in range(days):
        day = start + timedelta(days=offset)
        labels.append(day.strftime("%d %b"))
        values.append(int(counts.get(str(day), 0)))
    return {"labels": labels, "values": values}


def topic_accuracy(user_id: int) -> list[dict]:
    rows = (
        db.session.query(
            AssessmentAttempt.topic,
            func.avg(AssessmentAttempt.percentage),
            func.count(AssessmentAttempt.id),
        )
        .filter(AssessmentAttempt.user_id == user_id)
        .group_by(AssessmentAttempt.topic)
        .all()
    )
    return [
        {"topic": topic, "accuracy": int(round(avg or 0)), "attempts": count}
        for topic, avg, count in rows
    ]


def improvement(user_id: int) -> dict:
    """Baseline vs post-learning vs retention performance per topic.

    Reported honestly as *measured performance change* — never as proof that
    the platform alone caused the improvement.
    """
    phases: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    rows = (
        db.session.query(
            AssessmentAttempt.topic, AssessmentAttempt.phase, AssessmentAttempt.percentage
        )
        .filter(AssessmentAttempt.user_id == user_id)
        .all()
    )
    for topic, phase, percentage in rows:
        phases[topic][phase].append(int(percentage or 0))

    result = []
    for topic, by_phase in phases.items():
        baseline = _avg(by_phase.get("baseline"))
        post = _avg(by_phase.get("post"))
        retention = _avg(by_phase.get("retention"))
        result.append(
            {
                "topic": topic,
                "baseline": baseline,
                "post": post,
                "retention": retention,
                "absolute_improvement": (post - baseline)
                if (baseline is not None and post is not None)
                else None,
            }
        )
    return {"topics": sorted(result, key=lambda row: row["topic"]), "has_data": bool(result)}


def _avg(values):
    if not values:
        return None
    return int(round(sum(values) / len(values)))


def lab_progress(user_id: int) -> list[dict]:
    rows = (
        db.session.query(Lab.level, func.count(func.distinct(LabAttempt.lab_id)))
        .join(Lab, Lab.id == LabAttempt.lab_id)
        .filter(LabAttempt.user_id == user_id, LabAttempt.passed.is_(True))
        .group_by(Lab.level)
        .all()
    )
    counts = {level: count for level, count in rows}
    totals = dict(
        db.session.query(Lab.level, func.count(Lab.id)).group_by(Lab.level).all()
    )
    labels, values, targets = [], [], []
    for level in ("basic", "intermediate", "advanced", "capstone"):
        labels.append(level.capitalize())
        values.append(int(counts.get(level, 0)))
        targets.append(int(totals.get(level, 0)))
    return {"labels": labels, "values": values, "targets": targets}


def streak_history(user_id: int, days: int = 30) -> dict:
    from app.models import StreakDay

    start = date.today() - timedelta(days=days - 1)
    rows = (
        StreakDay.query.filter(StreakDay.user_id == user_id, StreakDay.day >= start)
        .order_by(StreakDay.day)
        .all()
    )
    active = {row.day: row.activity_count for row in rows if row.qualified}
    labels, values = [], []
    for offset in range(days):
        day = start + timedelta(days=offset)
        labels.append(day.strftime("%d %b"))
        values.append(int(active.get(day, 0)))
    return {"labels": labels, "values": values, "active_days": len(active)}


def commonly_missed(user_id: int, limit: int = 5) -> list[dict]:
    """Labs attempted repeatedly without passing — the revision list."""
    rows = (
        db.session.query(Lab.title_en, Lab.number, func.max(LabAttempt.percentage))
        .join(Lab, Lab.id == LabAttempt.lab_id)
        .filter(LabAttempt.user_id == user_id, LabAttempt.passed.is_(False))
        .group_by(Lab.id, Lab.title_en, Lab.number)
        .order_by(func.max(LabAttempt.percentage).asc())
        .limit(limit)
        .all()
    )
    return [
        {"title": title, "number": number, "best_score": int(best or 0)}
        for title, number, best in rows
    ]


def achievement_progress(user_id: int) -> dict:
    total = Achievement.query.filter_by(is_active=True).count()
    earned = UserAchievement.query.filter_by(user_id=user_id).count()
    return {
        "earned": earned,
        "total": total,
        "percent": int(earned / total * 100) if total else 0,
    }


def learner_overview(user: User) -> dict:
    stats = gamification.user_stats(user)
    total_time = (
        db.session.query(func.coalesce(func.sum(UserProgress.time_spent_seconds), 0))
        .filter(UserProgress.user_id == user.id)
        .scalar()
        or 0
    )
    attempts = LabAttempt.query.filter_by(user_id=user.id).count()
    first_try = LabAttempt.query.filter(
        LabAttempt.user_id == user.id, LabAttempt.retry_count == 0, LabAttempt.passed.is_(True)
    ).count()
    avg_score = (
        db.session.query(func.coalesce(func.avg(LabAttempt.percentage), 0))
        .filter(LabAttempt.user_id == user.id, LabAttempt.percentage > 0)
        .scalar()
        or 0
    )
    hints = (
        db.session.query(func.coalesce(func.sum(UserProgress.hints_used), 0))
        .filter(UserProgress.user_id == user.id)
        .scalar()
        or 0
    )
    return {
        "stats": stats,
        "total_learning_seconds": int(total_time),
        "total_learning_minutes": int(total_time // 60),
        "lab_attempts": attempts,
        "first_attempt_success_rate": int(first_try / attempts * 100) if attempts else 0,
        "final_success_rate": int(stats["labs_completed"] / attempts * 100) if attempts else 0,
        "average_score": int(round(avg_score)),
        "hints_used": int(hints),
        "weekly_activity": weekly_activity(user.id),
        "lab_progress": lab_progress(user.id),
        "streak_history": streak_history(user.id),
        "topic_accuracy": topic_accuracy(user.id),
        "improvement": improvement(user.id),
        "commonly_missed": commonly_missed(user.id),
        "achievement_progress": achievement_progress(user.id),
    }


def learner_csv(user: User) -> str:
    """Downloadable CSV of the learner's own activity data."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["CyberQuest learning report"])
    writer.writerow(["User", user.display_name or user.username])
    writer.writerow(["Generated", utcnow().isoformat(timespec="seconds")])
    writer.writerow([])
    writer.writerow(["Item type", "Item ID", "Status", "Best score", "Attempts",
                     "Hints used", "Seconds spent", "Completed at"])
    rows = (
        UserProgress.query.filter_by(user_id=user.id)
        .order_by(UserProgress.item_type, UserProgress.item_id)
        .all()
    )
    for row in rows:
        writer.writerow(
            [
                row.item_type,
                row.item_id,
                row.status,
                row.best_score,
                row.attempts_count,
                row.hints_used,
                row.time_spent_seconds,
                row.completed_at.isoformat(timespec="seconds") if row.completed_at else "",
            ]
        )
    writer.writerow([])
    writer.writerow(["XP reason", "XP"])
    for entry in gamification.xp_breakdown(user.id):
        writer.writerow([entry["reason"], entry["xp"]])
    return buffer.getvalue()


# ---------------------------------------------------------------------------
# Administrator analytics
# ---------------------------------------------------------------------------

def admin_overview() -> dict:
    total_users = User.query.count()
    learners = User.query.join(User.role).filter_by(name=ROLE_LEARNER).count()
    active_7d = (
        db.session.query(func.count(func.distinct(LearningEvent.user_id)))
        .filter(LearningEvent.created_at >= utcnow() - timedelta(days=7))
        .scalar()
        or 0
    )
    active_30d = (
        db.session.query(func.count(func.distinct(LearningEvent.user_id)))
        .filter(LearningEvent.created_at >= utcnow() - timedelta(days=30))
        .scalar()
        or 0
    )
    lab_attempts = LabAttempt.query.count()
    lab_passes = LabAttempt.query.filter(LabAttempt.passed.is_(True)).count()
    certificates = Certificate.query.filter(Certificate.revoked.is_(False)).count()

    videos_total = VideoAsset.query.count()
    videos_started = UserProgress.query.filter_by(item_type="video").count()
    comics_total = Comic.query.count()
    comics_read = UserProgress.query.filter_by(item_type="comic", status="completed").count()

    daily = (
        db.session.query(func.date(LearningEvent.created_at), func.count(LearningEvent.id))
        .filter(LearningEvent.created_at >= utcnow() - timedelta(days=14))
        .group_by(func.date(LearningEvent.created_at))
        .order_by(func.date(LearningEvent.created_at))
        .all()
    )

    return {
        "registered_users": total_users,
        "learners": learners,
        "active_7d": int(active_7d),
        "active_30d": int(active_30d),
        "lab_attempts": lab_attempts,
        "lab_pass_rate": int(lab_passes / lab_attempts * 100) if lab_attempts else 0,
        "certificates_issued": certificates,
        "videos_total": videos_total,
        "videos_started": videos_started,
        "comics_total": comics_total,
        "comics_read": comics_read,
        "daily_activity": {
            "labels": [str(day) for day, _ in daily],
            "values": [int(count) for _, count in daily],
        },
        "pending_news": CyberNews.query.filter_by(review_state="pending").count(),
        "published_news": CyberNews.query.filter_by(review_state="approved").count(),
    }


def hardest_labs(limit: int = 8) -> list[dict]:
    """Labs with the lowest pass rate — where learners struggle most."""
    rows = (
        db.session.query(
            Lab.number,
            Lab.title_en,
            func.count(LabAttempt.id),
            func.sum(db.case((LabAttempt.passed.is_(True), 1), else_=0)),
        )
        .join(LabAttempt, LabAttempt.lab_id == Lab.id)
        .group_by(Lab.id, Lab.number, Lab.title_en)
        .having(func.count(LabAttempt.id) >= 1)
        .all()
    )
    result = []
    for number, title, attempts, passes in rows:
        attempts = int(attempts or 0)
        passes = int(passes or 0)
        result.append(
            {
                "number": number,
                "title": title,
                "attempts": attempts,
                "passes": passes,
                "pass_rate": int(passes / attempts * 100) if attempts else 0,
            }
        )
    return sorted(result, key=lambda row: row["pass_rate"])[:limit]
