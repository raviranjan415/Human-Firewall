"""Gamified challenge pages.

Scenario answers are graded by ``app.api`` against stored data. Correct
answers are never sent to the browser before the learner commits to a choice.
"""

from __future__ import annotations

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Game, GameScenario, UserProgress
from app.services import progress as progress_service
from app.services.i18n import current_locale

games_bp = Blueprint("games", __name__)


def _completed_ids() -> set[int]:
    rows = (
        db.session.query(UserProgress.item_id)
        .filter_by(user_id=current_user.id, item_type="game", status="completed")
        .all()
    )
    return {row[0] for row in rows}


@games_bp.route("/")
@login_required
def index():
    games = Game.query.filter_by(state="published").order_by(Game.order_index).all()
    game_ids = [game.id for game in games]
    progress_records = (
        UserProgress.query.filter(
            UserProgress.user_id == current_user.id,
            UserProgress.item_type == "game",
            UserProgress.item_id.in_(game_ids),
        ).all()
        if game_ids
        else []
    )
    best_scores = {record.item_id: record for record in progress_records}
    completed = {
        record.item_id for record in progress_records if record.status == "completed"
    }

    return render_template(
        "games/index.html",
        games=games,
        completed=completed,
        best_scores=best_scores,
    )


@games_bp.route("/<slug>")
@login_required
def play(slug: str):
    game = Game.query.filter_by(slug=slug, state="published").first_or_404()
    scenarios = (
        GameScenario.query.filter_by(game_id=game.id)
        .order_by(GameScenario.order_index)
        .all()
    )

    locale = current_locale()
    # Only the prompt and the answer options are sent to the client. The
    # correct answer, explanation and warning signs are withheld until the
    # learner submits that scenario.
    payload = []
    for scenario in scenarios:
        payload.append(
            {
                "id": scenario.id,
                "type": scenario.scenario_type,
                "sender": scenario.sender,
                "subject": getattr(scenario, f"subject_{locale}", None)
                or scenario.subject_en,
                "body": getattr(scenario, f"body_{locale}", None) or scenario.body_en,
                "choices": [
                    {
                        "id": choice.id,
                        "text": getattr(choice, f"text_{locale}", None)
                        or choice.text_en,
                    }
                    for choice in scenario.choices
                ],
            }
        )

    record = progress_service.get_progress(current_user.id, "game", game.id)
    return render_template(
        "games/play.html",
        game=game,
        scenario_count=len(scenarios),
        scenarios_json=payload,
        record=record,
        page=request.args.get("p"),
    )
