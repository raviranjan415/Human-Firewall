"""Practical labs: prerequisites, server-side scoring and XP settlement."""

from __future__ import annotations

import json

import pytest

from app.models import Lab, LabAttempt, User
from app.services import labs as labs_service

from .conftest import login


def published_labs():
    """Every authored (published) lab, ordered by number."""
    return Lab.query.filter_by(state="published").order_by(Lab.number).all()


def _config(lab: Lab) -> dict:
    return json.loads(lab.validation_json or "{}")


def correct_answer(lab: Lab):
    """Build a fully correct submission from the stored configuration."""
    config = _config(lab)
    correct = config.get("correct", [])
    if lab.task_type == "single_choice":
        return correct[0] if isinstance(correct, list) else correct
    if lab.task_type == "order":
        return list(correct)
    if lab.task_type == "text_judgement":
        return " ".join(config.get("keywords", []))
    return list(correct)


def wrong_answer(lab: Lab):
    if lab.task_type == "single_choice":
        return "__definitely-not-the-answer__"
    if lab.task_type == "text_judgement":
        return "nothing relevant at all"
    return []


def test_lab_catalogue_is_seeded_honestly(app):
    published = published_labs()
    assert len(published) >= 1
    # Labs 11-100 exist as roadmap entries and must not be learner-visible.
    roadmap = Lab.query.filter_by(state="draft").all()
    assert roadmap, "the planned lab roadmap should be seeded in draft state"
    for lab in roadmap:
        assert lab.task_en is None
    for lab in published:
        assert lab.task_en and lab.task_type


def test_draft_labs_are_not_reachable(client, learner):
    draft = Lab.query.filter_by(state="draft").first()
    login(client, "learner1")
    assert client.get(f"/labs/{draft.id}").status_code == 404


def test_lab_quest_map_renders_for_a_signed_in_learner(client, learner):
    login(client, "learner1")
    response = client.get("/labs/")
    assert response.status_code == 200
    assert response.get_data(as_text=True)


def test_first_lab_is_unlocked_for_a_new_learner(app, learner):
    first = Lab.query.filter_by(number=1).first()
    assert labs_service.unlock_status(learner, first)["unlocked"] is True


def test_later_labs_stay_locked_until_the_previous_one_passes(app, learner):
    second = Lab.query.filter_by(number=2).first()
    status = labs_service.unlock_status(learner, second)
    assert status["unlocked"] is False
    assert status["reason"] == "prerequisite"

    first = Lab.query.filter_by(number=1).first()
    labs_service.submit_lab(learner, first, correct_answer(first))

    refreshed = User.query.get(learner.id)
    status = labs_service.unlock_status(refreshed, second)
    assert status["unlocked"] is True


def test_opening_a_lab_does_not_mark_it_complete(client, learner, db):
    first = Lab.query.filter_by(number=1).first()
    login(client, "learner1")
    assert client.get(f"/labs/{first.id}").status_code == 200

    db.session.expire_all()
    attempt = LabAttempt.query.filter_by(user_id=learner.id, lab_id=first.id).first()
    assert attempt is None or attempt.passed is False
    assert labs_service.passed_lab_ids(User.query.get(learner.id)) == set()


def test_locked_lab_page_explains_the_prerequisite(client, learner):
    second = Lab.query.filter_by(number=2).first()
    login(client, "learner1")
    response = client.get(f"/labs/{second.id}")
    assert response.status_code == 200
    assert second.title_en in response.get_data(as_text=True)


def test_submitting_to_a_locked_lab_is_refused_with_409(client, learner):
    second = Lab.query.filter_by(number=2).first()
    login(client, "learner1")
    response = client.post(
        f"/api/labs/{second.id}/submit",
        json={"answer": correct_answer(second), "hints_used": 0},
    )
    assert response.status_code == 409
    assert response.get_json()["error"] == "locked"


@pytest.mark.parametrize("task_type", ["single_choice", "multi_select", "order", "text_judgement"])
def test_scoring_accepts_the_correct_answer(app, task_type):
    lab = Lab.query.filter_by(task_type=task_type, state="published").first()
    if lab is None:
        pytest.skip(f"no published {task_type} lab is authored yet")
    percentage, feedback_en, feedback_hi, _ = labs_service.evaluate_submission(
        lab, correct_answer(lab)
    )
    assert percentage >= (lab.pass_score or 70), f"{task_type}: {feedback_en}"
    assert feedback_en and feedback_hi


@pytest.mark.parametrize("task_type", ["single_choice", "multi_select", "order", "text_judgement"])
def test_scoring_rejects_a_wrong_answer(app, task_type):
    lab = Lab.query.filter_by(task_type=task_type, state="published").first()
    if lab is None:
        pytest.skip(f"no published {task_type} lab is authored yet")
    percentage, *_ = labs_service.evaluate_submission(lab, wrong_answer(lab))
    assert percentage < (lab.pass_score or 70)


def test_every_authored_lab_is_passable(app):
    """A learner holding the intended answer must be able to pass every lab."""
    for lab in published_labs():
        percentage, *_ = labs_service.evaluate_submission(lab, correct_answer(lab))
        assert percentage >= (lab.pass_score or 70), (
            f"Lab {lab.number} ({lab.slug}) is not passable with its stored answer"
        )


def test_correct_submission_passes_and_credits_xp(client, learner, db):
    first = Lab.query.filter_by(number=1).first()
    login(client, "learner1")

    response = client.post(
        f"/api/labs/{first.id}/submit",
        json={"answer": correct_answer(first), "hints_used": 0},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["passed"] is True
    assert data["percentage"] >= first.pass_score
    # Basic labs pay the base reward and a perfect score adds the bonus.
    assert data["xp_awarded"] >= first.xp_reward
    assert data["next_lab_id"] is not None


def test_lab_xp_is_never_paid_twice(client, learner, db):
    first = Lab.query.filter_by(number=1).first()
    login(client, "learner1")
    payload = {"answer": correct_answer(first), "hints_used": 0}

    client.post(f"/api/labs/{first.id}/submit", json=payload)
    second = client.post(f"/api/labs/{first.id}/submit", json=payload)
    assert second.status_code == 200
    assert second.get_json()["xp_awarded"] == 0


def test_wrong_submission_awards_no_xp_and_can_be_retried(client, learner, db):
    first = Lab.query.filter_by(number=1).first()
    login(client, "learner1")

    failed = client.post(
        f"/api/labs/{first.id}/submit",
        json={"answer": wrong_answer(first), "hints_used": 0},
    )
    assert failed.status_code == 200
    assert failed.get_json()["passed"] is False
    assert failed.get_json()["xp_awarded"] == 0

    retried = client.post(
        f"/api/labs/{first.id}/submit",
        json={"answer": correct_answer(first), "hints_used": 0},
    )
    assert retried.get_json()["passed"] is True
    assert retried.get_json()["xp_awarded"] > 0


def test_intermediate_level_needs_thirty_passed_labs(app, learner):
    lab = Lab.query.filter_by(number=31).first()
    status = labs_service.unlock_status(learner, lab)
    assert status["unlocked"] is False
    assert status["reason"] == "level"
    assert status["missing_labs"] == 30


def test_passing_a_lab_cannot_be_forged_from_the_client(client, learner, db):
    """A learner may not skip a lab by posting straight to the next one."""
    first = Lab.query.filter_by(number=1).first()
    third = Lab.query.filter_by(number=3).first()
    login(client, "learner1")

    client.post(
        f"/api/labs/{third.id}/submit",
        json={"answer": correct_answer(third), "hints_used": 0},
    )
    db.session.expire_all()
    passed = labs_service.passed_lab_ids(User.query.get(learner.id))
    assert first.id not in passed
    assert third.id not in passed


def test_lab_recommendations_only_offer_unlocked_labs(app, learner, db):
    ready = labs_service.recommendations(learner, limit=1)
    assert ready
    assert ready[0].number == 1
