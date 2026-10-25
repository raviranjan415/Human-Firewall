"""Learning content pages: paths, video lessons and comic library.

Pages are read-only. Every action that changes progress or awards XP goes
through ``app.api`` and is validated on the server.
"""

from __future__ import annotations

import json

from flask import Blueprint, abort, render_template, request
from flask_login import current_user, login_required

from app.extensions import db
from app.models import (
    Comic,
    Lab,
    LearningPath,
    Lesson,
    Module,
    Question,
    UserProgress,
    VideoAsset,
)
from app.services import progress as progress_service
from app.services.i18n import current_locale

learning_bp = Blueprint("learning", __name__)


def _completed_ids(item_type: str) -> set[int]:
    rows = (
        db.session.query(UserProgress.item_id)
        .filter_by(user_id=current_user.id, item_type=item_type, status="completed")
        .all()
    )
    return {row[0] for row in rows}


def _localized_options(raw: str | None) -> list[str]:
    """Resolve a bilingual JSON option list into the active locale."""
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
            resolved.append(item.get(locale) or item.get("en") or "")
        else:
            resolved.append(str(item))
    return resolved


@learning_bp.route("/")
@login_required
def index():
    """Learning hub: the path, its modules, and every lesson inside them."""
    path = (
        LearningPath.query.filter_by(state="published")
        .order_by(LearningPath.order_index)
        .first()
    )
    modules = []
    if path is not None:
        modules = (
            Module.query.filter_by(path_id=path.id, state="published")
            .order_by(Module.order_index)
            .all()
        )
    return render_template(
        "learning/index.html",
        path=path,
        modules=modules,
        completed_lessons=_completed_ids("video"),
        completed_comics=_completed_ids("comic"),
    )


@learning_bp.route("/videos")
@login_required
def videos():
    category = (request.args.get("category") or "").strip()
    difficulty = (request.args.get("difficulty") or "").strip()

    query = VideoAsset.query.join(VideoAsset.lesson).filter(Lesson.state == "published")
    if category:
        query = query.filter(Lesson.category == category)
    if difficulty:
        query = query.filter(Lesson.difficulty == difficulty)

    assets = query.order_by(Lesson.order_index, VideoAsset.order_index).all()
    categories = [
        row[0]
        for row in db.session.query(Lesson.category)
        .filter(Lesson.state == "published", Lesson.category.isnot(None))
        .distinct()
        .order_by(Lesson.category)
        .all()
    ]
    return render_template(
        "learning/videos.html",
        assets=assets,
        categories=categories,
        completed=_completed_ids("video"),
        selected_category=category,
        selected_difficulty=difficulty,
    )


@learning_bp.route("/videos/<int:video_id>")
@learning_bp.route("/room/<int:video_id>")
@login_required
def video_detail(video_id: int):
    video = db.session.get(VideoAsset, video_id)
    if video is None or video.lesson is None or video.lesson.state != "published":
        abort(404)

    # Opening a lesson records "in progress" — never a completion.
    progress_service.start_activity(current_user, "video", video.id)
    db.session.commit()

    # Retrieve 100% topic-synchronized room content for this video and lesson:
    from app.services.lesson_sync import get_synchronized_room_content
    sync_content = get_synchronized_room_content(video, video.lesson)

    # Find matching comic for progress tracking:
    comic = (
        Comic.query.filter(Comic.title_en.ilike(f"%{video.title_en[:12]}%")).first()
        or Comic.query.filter_by(order_index=video.order_index).first()
        or Comic.query.filter_by(order_index=(video.order_index % 100)).first()
        or Comic.query.first()
    )

    # Find matching practical lab:
    lab = None
    if comic and comic.related_lab_id:
        lab = db.session.get(Lab, comic.related_lab_id)
    if lab is None:
        lab_num = ((video.order_index or 0) % 40) + 1
        lab = Lab.query.filter_by(number=lab_num).first() or Lab.query.first()

    questions = (
        Question.query.filter_by(lesson_id=video.lesson_id)
        .order_by(Question.order_index)
        .all()
    )

    return render_template(
        "learning/room.html",
        video=video,
        lesson=video.lesson,
        comic=comic,
        lab=lab,
        sync_comic=sync_content["comic"],
        sync_lab=sync_content["lab"],
        lab_payload=sync_content["lab"]["payload"],
        lab_options=sync_content["lab"]["options"],
        lab_json=json.dumps(sync_content["lab"]),
        video_scenes_json=json.dumps(sync_content["video_scenes"]),
        record=progress_service.get_progress(current_user.id, "video", video.id),
        comic_record=progress_service.get_progress(current_user.id, "comic", comic.id) if comic else None,
        questions=questions,
        questions_json=json.dumps(sync_content["questions"]),
        reading_material=sync_content["reading"],
        options_by_question={q.id: _localized_options(q.options_json) for q in questions},
    )


@learning_bp.route("/comics")
@login_required
def comics():
    collection = (request.args.get("collection") or "").strip()
    query = Comic.query.filter_by(state="published")
    if collection:
        query = query.filter(Comic.collection == collection)
    collections = [
        row[0]
        for row in db.session.query(Comic.collection)
        .filter(Comic.state == "published", Comic.collection.isnot(None))
        .distinct()
        .order_by(Comic.collection)
        .all()
    ]
    return render_template(
        "learning/comics.html",
        comics=query.order_by(Comic.order_index).all(),
        collections=collections,
        completed=_completed_ids("comic"),
        selected_collection=collection,
    )


@learning_bp.route("/comics/<slug>")
@login_required
def comic_detail(slug: str):
    comic = Comic.query.filter_by(slug=slug, state="published").first_or_404()
    return render_template(
        "learning/comic_detail.html",
        comic=comic,
        record=progress_service.get_progress(current_user.id, "comic", comic.id),
    )
