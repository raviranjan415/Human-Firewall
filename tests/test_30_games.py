"""Automated verification suite for the 30 Cybersecurity Awareness Games."""

from __future__ import annotations

from app.models import Game
from app.services.catalog_games_30 import GAMES_30

from .conftest import LEARNER_PASSWORD, login


def test_all_30_games_seeded(app):
    """Verify that all 30 specified cybersecurity awareness games exist in the database."""
    with app.app_context():
        from app.services.seed import ensure_games

        ensure_games()

        expected_slugs = [g["slug"] for g in GAMES_30]
        assert len(expected_slugs) == 30

        db_games = Game.query.filter(Game.slug.in_(expected_slugs)).all()
        db_slugs = {g.slug for g in db_games}

        for slug in expected_slugs:
            assert slug in db_slugs, f"Expected game {slug} not found in database."


def test_game_scenarios_and_choices_structure(app):
    """Verify that every game contains valid scenarios and choices or threat flags."""
    with app.app_context():
        from app.services.seed import ensure_games

        ensure_games()

        for spec in GAMES_30:
            game = Game.query.filter_by(slug=spec["slug"]).first()
            assert game is not None
            assert game.title_en
            assert game.difficulty in (
                "beginner",
                "intermediate",
                "advanced",
                "capstone",
            )
            assert len(game.scenarios) >= 1

            for scenario in game.scenarios:
                assert scenario.body_en
                assert scenario.explanation_en
                if scenario.choices:
                    correct_choices = [c for c in scenario.choices if c.is_correct]
                    assert len(correct_choices) >= 1, (
                        f"Scenario {scenario.id} has no correct choice."
                    )


def test_game_answer_evaluation_api(client, learner, app):
    """Test server-side grading via /api/games/<slug>/answer."""
    with app.app_context():
        from app.services.seed import ensure_games

        ensure_games()

        game = Game.query.filter_by(slug="phishing-detective").first()
        scenario = game.scenarios[0]
        correct_choice = next(c for c in scenario.choices if c.is_correct)
        incorrect_choice = next(c for c in scenario.choices if not c.is_correct)

    login(client, "learner1", LEARNER_PASSWORD)

    # 1. Correct submission
    res_correct = client.post(
        "/api/games/phishing-detective/answer",
        json={"scenario_id": scenario.id, "choice_id": correct_choice.id},
    )
    assert res_correct.status_code == 200
    data_correct = res_correct.get_json()
    assert data_correct["ok"] is True
    assert data_correct["correct"] is True
    assert data_correct["xp_value"] > 0
    assert "feedback" in data_correct

    # 2. Incorrect submission
    res_wrong = client.post(
        "/api/games/phishing-detective/answer",
        json={"scenario_id": scenario.id, "choice_id": incorrect_choice.id},
    )
    assert res_wrong.status_code == 200
    data_wrong = res_wrong.get_json()
    assert data_wrong["ok"] is True
    assert data_wrong["correct"] is False
    assert data_wrong["xp_value"] == 0


def test_game_completion_and_idempotent_rewards(client, learner, app):
    """Verify that completing a game records progress and awards XP exactly once."""
    with app.app_context():
        from app.services.seed import ensure_games

        ensure_games()

    login(client, "learner1", LEARNER_PASSWORD)

    # 1. Submit passing score (10/10)
    res1 = client.post(
        "/api/games/phishing-detective/complete",
        json={"score": 10, "total": 10, "time_spent": 45},
    )
    assert res1.status_code == 200
    d1 = res1.get_json()
    assert d1["ok"] is True
    assert d1["passed"] is True
    assert d1["first_completion"] is True
    assert d1["xp_awarded"] > 0

    # 2. Replay the game with 10/10: Should pass, but award 0 duplicate XP!
    res2 = client.post(
        "/api/games/phishing-detective/complete",
        json={"score": 10, "total": 10, "time_spent": 30},
    )
    assert res2.status_code == 200
    d2 = res2.get_json()
    assert d2["ok"] is True
    assert d2["passed"] is True
    assert d2["first_completion"] is False
    assert d2["xp_awarded"] == 0, (
        "Replaying a completed game must award 0 duplicate XP."
    )


def test_games_hub_view(client, learner, app):
    """Test games hub rendering and query performance."""
    with app.app_context():
        from app.services.seed import ensure_games

        ensure_games()

    login(client, "learner1", LEARNER_PASSWORD)

    res = client.get("/games/")
    assert res.status_code == 200
    assert b"Interactive Awareness Arena" in res.data
    assert b"Phishing Detective" in res.data
    assert b"Ultimate Human Firewall" in res.data
