"""XP ledger, progress tracking, streaks, levels and achievements."""

from __future__ import annotations

from datetime import date, timedelta

from app.models import (
    Achievement,
    LearningEvent,
    StreakDay,
    User,
    UserAchievement,
    UserProgress,
    VideoAsset,
    XPTransaction,
)
from app.services import gamification
from app.services import progress as progress_service

from .conftest import login
from .test_labs import correct_answer


def test_level_curve_is_transparent(app):
    assert gamification.level_for_xp(0) == 1
    assert gamification.level_for_xp(99) == 1
    assert gamification.level_for_xp(100) == 2
    assert gamification.level_for_xp(399) == 2
    assert gamification.level_for_xp(400) == 3
    assert gamification.xp_for_level(1) == 0
    assert gamification.xp_for_level(2) == 100
    assert gamification.xp_for_level(3) == 400


def test_award_xp_is_idempotent_for_the_same_event(app, learner, db):
    first = gamification.award_xp(
        learner, 50, reason="lab_basic", reference_type="lab", reference_id="lab:999"
    )
    second = gamification.award_xp(
        learner, 50, reason="lab_basic", reference_type="lab", reference_id="lab:999"
    )
    assert first == 50
    assert second == 0

    db.session.expire_all()
    assert User.query.get(learner.id).xp_total == 50
    assert XPTransaction.query.filter_by(user_id=learner.id).count() == 1


def test_rewarding_zero_or_negative_amounts_is_a_no_op(app, learner):
    assert gamification.award_xp(learner, 0, reason="nothing") == 0
    assert gamification.award_xp(learner, -10, reason="nothing") == 0
    assert XPTransaction.query.filter_by(user_id=learner.id).count() == 0


def test_video_completion_pays_the_configured_reward_once(client, learner, app, db):
    video = VideoAsset.query.first()
    assert video is not None
    login(client, "learner1")

    first = client.post(f"/api/videos/{video.id}/complete", json={"time_spent": 300})
    assert first.status_code == 200
    assert first.get_json()["xp_awarded"] == app.config["XP_REWARDS"]["video_lesson"]
    assert first.get_json()["first_completion"] is True

    second = client.post(f"/api/videos/{video.id}/complete", json={"time_spent": 300})
    assert second.get_json()["xp_awarded"] == 0


def test_video_position_progress_is_recorded(client, learner, db):
    video = VideoAsset.query.first()
    login(client, "learner1")

    response = client.post(
        f"/api/videos/{video.id}/progress", json={"position": 60, "duration": 240}
    )
    assert response.status_code == 200
    assert response.get_json()["progress_percent"] == 25

    db.session.expire_all()
    record = UserProgress.query.filter_by(
        user_id=learner.id, item_type="video", item_id=video.id
    ).first()
    assert record is not None
    assert record.status == "in_progress"
    assert record.last_position_seconds == 60


def test_comic_completion_awards_xp_once(client, learner, app, db):
    from app.models import Comic

    comic = Comic.query.filter_by(state="published").first()
    login(client, "learner1")

    first = client.post(f"/api/comics/{comic.id}/complete", json={})
    assert first.status_code == 200
    assert first.get_json()["xp_awarded"] == app.config["XP_REWARDS"]["comic"]
    assert client.post(f"/api/comics/{comic.id}/complete", json={}).get_json()["xp_awarded"] == 0


def test_completion_records_a_streak_day(app, learner, db):
    progress_service.complete_activity(learner, "comic", 424242, event_type="comic_read")

    db.session.expire_all()
    refreshed = User.query.get(learner.id)
    assert StreakDay.query.filter_by(user_id=learner.id).count() == 1
    assert refreshed.current_streak == 1
    assert refreshed.longest_streak == 1
    assert refreshed.last_activity_date == date.today()


def test_consecutive_days_build_a_longer_streak(app, learner, db):
    for offset in (2, 1, 0):
        gamification.record_streak_activity(
            learner, day=date.today() - timedelta(days=offset)
        )
    db.session.commit()
    refreshed = User.query.get(learner.id)
    assert refreshed.current_streak == 3
    assert refreshed.longest_streak == 3


def test_a_gap_breaks_the_current_streak_but_keeps_the_longest(app, learner, db):
    for offset in (5, 4, 3):
        gamification.record_streak_activity(
            learner, day=date.today() - timedelta(days=offset)
        )
    # Re-anchor the counters on the real today so the gap is measured.
    gamification._recalculate_streak_counters(learner, date.today())
    db.session.commit()
    db.session.expire_all()
    refreshed = User.query.get(learner.id)
    assert refreshed.current_streak == 0
    assert refreshed.longest_streak == 3


def test_lab_passing_unlocks_the_first_steps_achievement(client, learner, db):
    from app.models import Lab

    first = Lab.query.filter_by(number=1).first()

    login(client, "learner1")
    response = client.post(
        f"/api/labs/{first.id}/submit",
        json={"answer": correct_answer(first), "hints_used": 0},
    )
    codes = response.get_json()["achievements"]
    assert "first_steps" in codes
    assert UserAchievement.query.filter_by(user_id=learner.id).count() >= 1


def test_achievements_are_awarded_only_once(app, learner, db):
    achievement = Achievement.query.filter_by(code="first_steps").first()
    assert achievement is not None

    progress_service.complete_activity(learner, "comic", 909090, event_type="comic_read")
    from app.models import Lab, LabAttempt

    lab = Lab.query.filter_by(number=1).first()
    db.session.add(
        LabAttempt(
            user_id=learner.id,
            lab_id=lab.id,
            passed=True,
            percentage=100,
            score=100,
            max_score=100,
            status="passed",
        )
    )
    db.session.commit()

    gamification.evaluate_achievements(learner)
    gamification.evaluate_achievements(learner)
    assert UserAchievement.query.filter_by(
        user_id=learner.id, achievement_id=achievement.id
    ).count() == 1


def test_xp_breakdown_sums_the_ledger(app, learner, db):
    gamification.award_xp(learner, 30, reason="lab_basic", reference_id="lab:1")
    gamification.award_xp(learner, 20, reason="video_lesson", reference_id="video:1")
    gamification.award_xp(learner, 20, reason="video_lesson", reference_id="video:2")

    rows = {row["reason"]: row["xp"] for row in gamification.xp_breakdown(learner.id)}
    assert rows["lab_basic"] == 30
    assert rows["video_lesson"] == 40


def test_leaderboard_exposes_only_display_names(app, learner, db):
    gamification.award_xp(learner, 120, reason="lab_basic", reference_id="lab:1")
    rows = gamification.leaderboard(scope="global", limit=10)
    assert rows
    top = rows[0]
    assert set(top) == {"rank", "user_id", "name", "xp", "level"}
    assert "email" not in top


def test_learner_summary_api_reflects_real_progress(client, learner, db):
    gamification.award_xp(learner, 150, reason="lab_basic", reference_id="lab:1")
    db.session.commit()

    login(client, "learner1")
    response = client.get("/api/me/summary")
    assert response.status_code == 200
    body = response.get_json()
    assert body["xp"] == 150
    assert body["level"] == 2
    assert body["level_info"]["level"] == 2


def test_failed_attempts_are_logged_without_punishment(app, learner, db):
    progress_service.record_failure(learner, "lab", 1, score=20)
    db.session.expire_all()

    assert LearningEvent.query.filter_by(
        user_id=learner.id, event_type="activity_failed"
    ).count() == 1
    assert XPTransaction.query.filter_by(user_id=learner.id).count() == 0
    record = UserProgress.query.filter_by(
        user_id=learner.id, item_type="lab", item_id=1
    ).first()
    assert record.status == "in_progress"
    assert record.first_attempt_passed is False
