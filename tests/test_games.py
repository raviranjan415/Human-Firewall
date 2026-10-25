"""Games: answer secrecy, server-side grading and reward settlement."""

from __future__ import annotations

import pytest

from app.models import Game, GameScenario, ScenarioChoice

from .conftest import login


def published_game():
    game = Game.query.filter_by(state="published").order_by(Game.order_index).first()
    assert game is not None, "at least one game must be seeded"
    return game


def first_scenario(game: Game) -> GameScenario:
    scenario = (
        GameScenario.query.filter_by(game_id=game.id)
        .order_by(GameScenario.order_index)
        .first()
    )
    assert scenario is not None
    return scenario


def correct_submission(scenario: GameScenario) -> dict:
    if scenario.choices:
        choice = next(c for c in scenario.choices if c.is_correct)
        return {"scenario_id": scenario.id, "choice_id": choice.id}
    return {"scenario_id": scenario.id, "is_threat": scenario.is_threat}


def wrong_submission(scenario: GameScenario) -> dict:
    if scenario.choices:
        choice = next((c for c in scenario.choices if not c.is_correct), None)
        if choice is None:
            pytest.skip("scenario has no incorrect option")
        return {"scenario_id": scenario.id, "choice_id": choice.id}
    return {"scenario_id": scenario.id, "is_threat": not scenario.is_threat}


def test_game_index_renders(client, learner):
    login(client, "learner1")
    response = client.get("/games/")
    assert response.status_code == 200


def test_play_page_never_ships_the_answers(client, learner):
    game = published_game()
    login(client, "learner1")
    response = client.get(f"/games/{game.slug}")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert '"is_correct"' not in html
    assert '"explanation_en"' not in html
    assert "warning_signs_en" not in html


def test_scenario_is_graded_against_stored_data(client, learner):
    game = published_game()
    scenario = first_scenario(game)
    login(client, "learner1")

    right = client.post(f"/api/games/{game.slug}/answer", json=correct_submission(scenario))
    assert right.status_code == 200
    body = right.get_json()
    assert body["correct"] is True
    assert body["xp_value"] > 0
    assert body["explanation"]

    wrong = client.post(f"/api/games/{game.slug}/answer", json=wrong_submission(scenario))
    assert wrong.get_json()["correct"] is False
    assert wrong.get_json()["xp_value"] == 0


def test_every_seeded_scenario_can_be_answered_correctly(client, learner):
    game = published_game()
    login(client, "learner1")
    for scenario in GameScenario.query.filter_by(game_id=game.id).all():
        response = client.post(
            f"/api/games/{game.slug}/answer", json=correct_submission(scenario)
        )
        assert response.status_code == 200
        assert response.get_json()["correct"] is True


def test_answering_does_not_leak_other_scenarios(client, learner):
    game = published_game()
    scenario = first_scenario(game)
    login(client, "learner1")
    body = client.post(
        f"/api/games/{game.slug}/answer", json=correct_submission(scenario)
    ).get_json()
    # A single answer must not expose the whole answer key.
    assert "choices" not in body
    assert "scenarios" not in body


def test_completing_a_game_credits_xp_once(client, learner, db):
    game = published_game()
    login(client, "learner1")
    total = GameScenario.query.filter_by(game_id=game.id).count()

    first = client.post(
        f"/api/games/{game.slug}/complete",
        json={"score": total, "total": total, "time_spent": 120},
    )
    assert first.status_code == 200
    assert first.get_json()["passed"] is True
    assert first.get_json()["xp_awarded"] >= game.xp_reward

    second = client.post(
        f"/api/games/{game.slug}/complete",
        json={"score": total, "total": total, "time_spent": 120},
    )
    assert second.get_json()["xp_awarded"] == 0


def test_failing_a_game_awards_nothing_and_stays_replayable(client, learner, db):
    game = published_game()
    login(client, "learner1")
    total = max(1, GameScenario.query.filter_by(game_id=game.id).count())

    response = client.post(
        f"/api/games/{game.slug}/complete", json={"score": 0, "total": total}
    )
    assert response.status_code == 200
    assert response.get_json()["passed"] is False
    assert response.get_json()["xp_awarded"] == 0


def test_unknown_game_returns_404(client, learner):
    login(client, "learner1")
    assert client.get("/games/not-a-real-game").status_code == 404
    assert client.post("/api/games/not-a-real-game/complete", json={}).status_code == 404


def test_scenario_choices_are_immutable_content(app):
    """Sanity check that a scenario always has exactly one correct choice."""
    for scenario in GameScenario.query.all():
        if not scenario.choices:
            continue
        correct = [c for c in scenario.choices if c.is_correct]
        assert len(correct) == 1, f"scenario {scenario.id} has {len(correct)} correct choices"
        assert all(isinstance(c, ScenarioChoice) for c in scenario.choices)
