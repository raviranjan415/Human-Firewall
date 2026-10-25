"""User dashboard, leaderboard, achievements and daily challenge pages."""

from __future__ import annotations

from datetime import date

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.extensions import db
from app.models import (
    Achievement,
    Comic,
    Game,
    HistoricalIncident,
    Lab,
    Notification,
    UserAchievement,
    VideoAsset,
)
from app.services import analytics
from app.services import gamification
from app.services import labs as labs_service
from app.services import progress as progress_service

dashboard_bp = Blueprint("dashboard", __name__)


def _daily_challenge() -> dict | None:
    """A stable, date-based challenge — the same for everyone all day."""
    labs = Lab.query.filter_by(state="published").order_by(Lab.number).all()
    if labs:
        index = date.today().toordinal() % len(labs)
        return {"kind": "lab", "lab": labs[index], "xp": labs[index].xp_reward}
    return None


def _recommended_next() -> dict | None:
    """Prerequisite-aware recommendation driven by real progress."""
    ready = labs_service.recommendations(current_user, limit=1)
    if ready:
        return {"kind": "lab", "lab": ready[0]}

    game = Game.query.filter_by(state="published").order_by(Game.order_index).first()
    if game:
        return {"kind": "game", "game": game}

    video = (
        VideoAsset.query.join(VideoAsset.lesson)
        .order_by(VideoAsset.id)
        .first()
    )
    if video:
        return {"kind": "video", "video": video}
    return None


@dashboard_bp.route("/")
@login_required
def index():
    from app.models import UserProgress

    summary = progress_service.summary(current_user)
    level_info = gamification.level_progress(current_user.xp_total or 0)
    milestone = progress_service.next_certificate_milestone(summary["labs_completed"])

    completed_videos = UserProgress.query.filter_by(
        user_id=current_user.id, item_type="video", status="completed"
    ).count()
    completed_comics = UserProgress.query.filter_by(
        user_id=current_user.id, item_type="comic", status="completed"
    ).count()

    recent_achievements = (
        UserAchievement.query.filter_by(user_id=current_user.id)
        .order_by(UserAchievement.awarded_at.desc())
        .limit(6)
        .all()
    )
    latest_incidents = (
        HistoricalIncident.query.filter_by(state="published")
        .order_by(HistoricalIncident.year.desc())
        .limit(3)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        summary=summary,
        level_info=level_info,
        milestone=milestone,
        completed_videos=completed_videos,
        completed_comics=completed_comics,
        recent_achievements=recent_achievements,
        latest_incidents=latest_incidents,
        daily=_daily_challenge(),
        weekly={
            "game": Game.query.filter_by(state="published").order_by(Game.order_index).first(),
        },
        recommended=_recommended_next(),
        mistakes=analytics.commonly_missed(current_user.id),
    )


@dashboard_bp.route("/challenges")
@login_required
def challenges():
    labs = Lab.query.filter_by(state="published").order_by(Lab.number).limit(5).all()
    games = Game.query.filter_by(state="published").order_by(Game.order_index).all()
    return render_template(
        "dashboard/challenges.html",
        daily=_daily_challenge(),
        labs=labs,
        games=games,
        comics=Comic.query.filter_by(state="published").order_by(Comic.order_index).limit(3).all(),
    )


@dashboard_bp.route("/leaderboard")
@login_required
def leaderboard():
    from flask import request

    scope = request.args.get("scope", "global")
    if scope not in gamification.VALID_SCOPES:
        scope = "global"
    return render_template(
        "dashboard/leaderboard.html",
        scope=scope,
        rows=gamification.leaderboard(scope, limit=25),
        my_rank=gamification.user_rank(current_user),
    )


@dashboard_bp.route("/achievements")
@login_required
def achievements():
    earned_ids = {
        row.achievement_id for row in UserAchievement.query.filter_by(user_id=current_user.id).all()
    }
    all_achievements = Achievement.query.filter_by(is_active=True).order_by(Achievement.id).all()
    return render_template(
        "dashboard/achievements.html",
        achievements=all_achievements,
        earned_ids=earned_ids,
        progress=gamification.user_stats(current_user),
    )


@dashboard_bp.route("/notifications/read", methods=["POST"])
@login_required
def mark_notifications_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({"is_read": True})
    db.session.commit()
    from flask import redirect, url_for

    return redirect(url_for("dashboard.index"))
