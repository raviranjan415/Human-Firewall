"""Authentication, session handling, lockout and role enforcement."""

from __future__ import annotations

from app.models import User
from app.models.user import ROLE_ADMIN, ROLE_LEARNER

from .conftest import ADMIN_PASSWORD, ADMIN_USERNAME, LEARNER_PASSWORD, login


def test_registration_creates_a_learner_and_signs_them_in(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "newbie",
            "email": "newbie@example.com",
            "display_name": "Newbie",
            "password": LEARNER_PASSWORD,
            "confirm_password": LEARNER_PASSWORD,
            "accept_terms": "y",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    user = User.query.filter_by(username="newbie").first()
    assert user is not None
    assert user.role_name == ROLE_LEARNER
    assert user.email == "newbie@example.com"

    with client.session_transaction() as session:
        assert session.get("_user_id") == str(user.id)


def test_registration_rejects_a_weak_password(client):
    client.post(
        "/auth/register",
        data={
            "username": "weakling",
            "email": "weakling@example.com",
            "password": "short",
            "confirm_password": "short",
            "accept_terms": "y",
        },
    )
    assert User.query.filter_by(username="weakling").first() is None


def test_registration_rejects_a_duplicate_username(client, learner):
    client.post(
        "/auth/register",
        data={
            "username": "learner1",
            "email": "another@example.com",
            "password": LEARNER_PASSWORD,
            "confirm_password": LEARNER_PASSWORD,
            "accept_terms": "y",
        },
    )
    assert User.query.filter_by(email="another@example.com").first() is None


def test_passwords_are_stored_only_as_salted_hashes(learner):
    assert learner.password_hash
    assert learner.password_hash != LEARNER_PASSWORD
    assert LEARNER_PASSWORD not in learner.password_hash
    assert learner.check_password(LEARNER_PASSWORD) is True
    assert learner.check_password("not-the-password") is False


def test_login_succeeds_with_username_or_email(client, learner):
    response = login(client, "learner1")
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert session.get("_user_id") == str(learner.id)

    client.post("/auth/logout")

    response = login(client, "learner1@example.com")
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert session.get("_user_id") == str(learner.id)


def test_login_failure_is_generic_and_does_not_sign_anyone_in(client, learner):
    response = client.post(
        "/auth/login",
        data={"identifier": "learner1", "password": "wrong-password"},
        follow_redirects=True,
    )
    assert b"Invalid credentials" in response.data
    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_login_failure_for_unknown_account_looks_identical(client, learner):
    """An unknown account must be indistinguishable from a wrong password."""
    unknown = client.post(
        "/auth/login",
        data={"identifier": "ghost@example.com", "password": "wrong-password"},
        follow_redirects=True,
    )

    known = client.post(
        "/auth/login",
        data={"identifier": "learner1", "password": "wrong-password"},
        follow_redirects=True,
    )

    assert unknown.status_code == known.status_code
    assert b"Invalid credentials" in unknown.data
    for hint in (b"no such", b"not found", b"does not exist", b"unknown account"):
        assert hint not in unknown.data.lower()
    # The only difference between the two pages is the echoed identifier.
    assert unknown.data.replace(b"ghost@example.com", b"") == known.data.replace(b"learner1", b"")


def test_account_is_locked_after_repeated_failures(client, learner):
    for _ in range(5):
        client.post(
            "/auth/login",
            data={"identifier": "learner1", "password": "wrong-password"},
        )

    fresh = User.query.filter_by(username="learner1").first()
    assert fresh.locked_until is not None

    response = client.post(
        "/auth/login",
        data={"identifier": "learner1", "password": LEARNER_PASSWORD},
        follow_redirects=True,
    )
    assert b"temporarily locked" in response.data
    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_logout_clears_the_session(client, learner):
    login(client, "learner1")
    response = client.post("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_dashboard_requires_authentication(client):
    response = client.get("/dashboard/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_learner_is_forbidden_from_the_admin_console(client, learner):
    login(client, "learner1")
    assert client.get("/admin/").status_code == 403
    assert client.get("/admin/users").status_code == 403


def test_administrator_can_reach_the_admin_console(client, admin_user):
    login(client, ADMIN_USERNAME, ADMIN_PASSWORD)
    assert client.get("/admin/").status_code == 200


def test_instructor_is_forbidden_from_the_admin_console(client, instructor):
    login(client, "instructor1")
    assert client.get("/admin/").status_code == 403


def test_deactivated_account_cannot_sign_in(client, learner, db):
    learner.is_active = False
    db.session.commit()

    response = client.post(
        "/auth/login",
        data={"identifier": "learner1", "password": LEARNER_PASSWORD},
        follow_redirects=True,
    )
    assert b"disabled" in response.data
    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_password_reset_request_never_reveals_whether_an_account_exists(client):
    known = client.post(
        "/auth/forgot", data={"email": "nobody@example.com"}, follow_redirects=True
    )
    assert known.status_code == 200
    assert b"If that account exists" in known.data


def test_password_reset_token_changes_the_password(client, learner, app):
    token = app.config["SECRET_KEY"]
    from app.auth.routes import _serializer

    signed = _serializer().dumps({"uid": learner.id})
    response = client.post(
        f"/auth/reset/{signed}",
        data={
            "password": "BrandNew1pass",
            "confirm_password": "BrandNew1pass",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    fresh = User.query.filter_by(username="learner1").first()
    assert fresh.check_password("BrandNew1pass") is True
    assert fresh.check_password(LEARNER_PASSWORD) is False


def test_invalid_reset_token_is_refused(client):
    response = client.get("/auth/reset/not-a-real-token", follow_redirects=True)
    assert b"not valid" in response.data


def test_role_constants_match_the_seeded_roles(app):
    from app.models import Role

    names = {row.name for row in Role.query.all()}
    assert {ROLE_LEARNER, ROLE_ADMIN} <= names
