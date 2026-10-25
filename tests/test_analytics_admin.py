"""Analytics pages plus administrator-only workflows and audit logging."""

from __future__ import annotations

from app.models import AuditLog, CyberNews, Lab, LabAttempt, User
from app.services import analytics

from .conftest import ADMIN_PASSWORD, ADMIN_USERNAME, LEARNER_PASSWORD, login, logout


def add_passing_attempt(user, lab, db, percentage=100):
    db.session.add(
        LabAttempt(
            user_id=user.id,
            lab_id=lab.id,
            percentage=percentage,
            score=percentage,
            max_score=100,
            passed=True,
            status="passed",
        )
    )
    db.session.commit()


# ---------------------------------------------------------------------------
# Learner analytics
# ---------------------------------------------------------------------------

def test_analytics_requires_authentication(client):
    response = client.get("/analytics/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_learner_analytics_page_renders(client, learner):
    login(client, "learner1")
    response = client.get("/analytics/")
    assert response.status_code == 200
    assert response.get_data(as_text=True)


def test_csv_export_is_a_download(client, learner):
    login(client, "learner1")
    response = client.get("/analytics/export.csv")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/csv")
    assert "attachment" in response.headers["Content-Disposition"]


def test_cohort_view_is_for_instructors_and_admins_only(client, learner, instructor):
    login(client, "learner1")
    assert client.get("/analytics/cohort").status_code == 403
    logout(client)

    login(client, "instructor1")
    assert client.get("/analytics/cohort").status_code == 200


def test_learner_overview_is_computed_from_recorded_activity(app, learner, db):
    lab = Lab.query.filter_by(number=1).first()
    add_passing_attempt(learner, lab, db)

    overview = analytics.learner_overview(learner)
    assert overview["stats"]["labs_completed"] == 1
    assert overview["lab_attempts"] == 1
    assert overview["average_score"] == 100
    assert "weekly_activity" in overview
    assert len(overview["weekly_activity"]["values"]) == 7


def test_commonly_missed_labs_are_derived_from_failed_attempts(app, learner, db):
    lab = Lab.query.filter_by(number=1).first()
    db.session.add(
        LabAttempt(
            user_id=learner.id, lab_id=lab.id, percentage=20, score=20,
            max_score=100, passed=False, status="failed",
        )
    )
    db.session.commit()

    rows = analytics.commonly_missed(learner.id)
    assert any(row["number"] == lab.number for row in rows)
    assert all(row["best_score"] < 70 for row in rows)


def test_hardest_labs_works_on_an_empty_dataset(app):
    assert isinstance(analytics.hardest_labs(), list)


# ---------------------------------------------------------------------------
# Administrator console
# ---------------------------------------------------------------------------

def test_admin_overview_renders(client, admin_user):
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    assert client.get("/admin/users").status_code == 200
    assert client.get("/admin/content").status_code == 200
    assert client.get("/admin/news").status_code == 200
    assert client.get("/admin/audit").status_code == 200


def test_admin_refuses_to_publish_an_unauthored_lab(client, admin_user, db):
    draft = Lab.query.filter_by(state="draft").first()
    assert draft is not None and draft.task_en is None

    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    response = client.post(
        f"/admin/content/labs/{draft.id}/state",
        data={"state": "published"},
        follow_redirects=True,
    )
    assert b"cannot be published" in response.data

    db.session.expire_all()
    assert Lab.query.filter_by(number=draft.number).first().state == "draft"


def test_publishing_an_authored_lab_is_audited(client, admin_user, db):
    lab = Lab.query.filter_by(number=1).first()
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)

    response = client.post(
        f"/admin/content/labs/{lab.id}/state",
        data={"state": "published"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    entry = AuditLog.query.filter_by(action="lab_state_changed").first()
    assert entry is not None
    assert entry.actor_id == admin_user.id
    assert entry.target_type == "lab"


def test_invalid_lab_state_is_rejected(client, admin_user, db):
    lab = Lab.query.filter_by(number=1).first()
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    response = client.post(
        f"/admin/content/labs/{lab.id}/state", data={"state": "not-a-state"}
    )
    assert response.status_code == 400


def test_admin_cannot_deactivate_their_own_account(client, admin_user, db):
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    response = client.post(
        f"/admin/users/{admin_user.id}/toggle", follow_redirects=True
    )
    assert b"cannot deactivate your own account" in response.data

    db.session.expire_all()
    assert User.query.get(admin_user.id).is_active is True


def test_admin_can_disable_and_reenable_a_learner(client, admin_user, learner, db):
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)

    client.post(f"/admin/users/{learner.id}/toggle", follow_redirects=True)
    db.session.expire_all()
    disabled = User.query.get(learner.id)
    assert disabled.is_active is False
    assert AuditLog.query.filter_by(action="user_active_toggled").count() == 1

    client.post(f"/admin/users/{learner.id}/toggle", follow_redirects=True)
    db.session.expire_all()
    assert User.query.get(learner.id).is_active is True


def test_admin_reviews_a_news_story(client, admin_user, db):
    story = CyberNews(
        title="Test advisory",
        url="https://example.com/advisory",
        content_hash="a" * 64,
        review_state="pending",
    )
    db.session.add(story)
    db.session.commit()

    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    response = client.post(
        f"/admin/news/{story.id}/review",
        data={"decision": "approved"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    db.session.expire_all()
    assert CyberNews.query.get(story.id).review_state == "approved"
    assert AuditLog.query.filter_by(action="news_reviewed").count() == 1


def test_pending_news_is_not_visible_to_learners(client, learner, db):
    db.session.add(
        CyberNews(
            title="Unreviewed rumour",
            url="https://example.com/rumour",
            content_hash="b" * 64,
            review_state="pending",
        )
    )
    db.session.commit()

    login(client, "learner1")
    response = client.get("/cyber-news/")
    assert response.status_code == 200
    assert b"Unreviewed rumour" not in response.data


def test_audit_log_never_records_credentials(client, admin_user, db):
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    client.post(
        f"/admin/users/{admin_user.id}/toggle",
        data={"password": LEARNER_PASSWORD},
        follow_redirects=True,
    )
    for entry in AuditLog.query.all():
        assert (entry.detail_json or "") == "" or LEARNER_PASSWORD not in entry.detail_json
