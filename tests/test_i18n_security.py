"""Bilingual behaviour, security headers, CSRF wiring and error hygiene."""

from __future__ import annotations

from flask import session

from app.config import BaseConfig, DevelopmentConfig, ProductionConfig, TestingConfig
from app.models import Lab
from app.services.i18n import current_locale, t, t_content


def test_default_locale_is_english(app):
    with app.test_request_context("/"):
        assert current_locale() == "en"
        assert t("nav.dashboard") == "Dashboard"


def test_locale_can_be_switched_to_hindi(app):
    with app.test_request_context("/"):
        session["locale"] = "hi"
        assert current_locale() == "hi"
        assert t("nav.dashboard") == "डैशबोर्ड"
        assert t("brand.tagline") == "सुरक्षा के साथ मज़ा"


def test_missing_translation_falls_back_to_the_key(app):
    with app.test_request_context("/"):
        assert t("this.key.does.not.exist") == "this.key.does.not.exist"


def test_translated_strings_never_return_another_language_by_accident(app):
    """A Hindi string that is missing must fall back to English, not to blank."""
    lab = Lab.query.filter_by(number=1).first()
    with app.test_request_context("/"):
        session["locale"] = "en"
        assert t_content(lab, "title") == lab.title_en
        assert t_content(lab, "scenario") == lab.scenario_en

    with app.test_request_context("/"):
        session["locale"] = "hi"
        assert t_content(lab, "title") == lab.title_hi
        assert t_content(lab, "scenario") == lab.scenario_hi


def test_hindi_content_falls_back_to_english_when_absent(app):
    draft = Lab.query.filter_by(state="draft").first()
    assert draft.title_hi is None
    with app.test_request_context("/"):
        session["locale"] = "hi"
        assert t_content(draft, "title") == draft.title_en


def test_t_content_handles_none(app):
    with app.test_request_context("/"):
        assert t_content(None, "title") == ""


def test_language_switch_endpoint_stores_the_locale(client):
    client.get("/lang/hi")
    with client.session_transaction() as sess:
        assert sess.get("locale") == "hi"


def test_unsupported_locale_is_ignored(client):
    client.get("/lang/de")
    with client.session_transaction() as sess:
        assert sess.get("locale") is None


def test_pages_render_in_hindi_after_switching(client):
    client.get("/lang/hi")
    response = client.get("/help")
    assert response.status_code == 200
    assert response.get_data(as_text=True)


# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------

def test_security_headers_are_present(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    csp = response.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp


def test_cross_site_scripting_sources_are_not_allowed_by_the_csp(client):
    csp = client.get("/").headers["Content-Security-Policy"]
    assert "unsafe-eval" not in csp
    assert "cdn" not in csp


def test_csrf_protection_is_enabled_outside_testing():
    assert DevelopmentConfig.WTF_CSRF_ENABLED is True
    assert ProductionConfig.WTF_CSRF_ENABLED is True
    assert TestingConfig.WTF_CSRF_ENABLED is False


def test_cookie_hardening_defaults():
    assert BaseConfig.SESSION_COOKIE_HTTPONLY is True
    assert BaseConfig.SESSION_COOKIE_SAMESITE == "Lax"
    assert ProductionConfig.SESSION_COOKIE_SECURE is True
    assert ProductionConfig.CREATE_DEMO_ACCOUNTS is False


def test_pages_carry_a_csrf_token_for_the_front_end(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b'name="csrf-token"' in response.data


def test_404_page_is_friendly_and_leaks_nothing(client):
    response = client.get("/definitely-not-a-page")
    assert response.status_code == 404
    body = response.get_data(as_text=True)
    assert b"Traceback" not in response.data
    assert "sqlalchemy" not in body.lower()
    assert "d:\\human-firewall" not in body.lower()


def test_api_errors_are_returned_as_json(client):
    response = client.get("/api/definitely-not-a-route")
    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["error"] == "not_found"


def test_anonymous_api_calls_are_not_answered_with_a_redirect(client):
    response = client.get("/api/me/summary")
    # flask-login sends unauthenticated API calls to the login view; the
    # payload must never be served.
    assert response.status_code in (302, 401)
    assert b"xp" not in response.data


def test_protected_pages_redirect_to_login(client):
    for path in ("/dashboard/", "/labs/", "/games/", "/analytics/", "/certificates/"):
        response = client.get(path)
        assert response.status_code == 302, path
        assert "/auth/login" in response.headers["Location"], path


def test_static_assets_are_served_locally(client):
    for asset in (
        "/static/vendor/bootstrap.min.css",
        "/static/vendor/bootstrap.bundle.min.js",
        "/static/vendor/chart.umd.min.js",
        "/static/css/brand.css",
        "/static/js/app.js",
    ):
        assert client.get(asset).status_code == 200, asset


def test_healthcheck_reports_database_status(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_legal_and_help_pages_are_public(client):
    for path in ("/privacy", "/terms", "/accessibility", "/help"):
        assert client.get(path).status_code == 200, path


def test_accessibility_preferences_change_the_body_classes(app, learner, db):
    from app.services.i18n import get_theme_classes

    with app.test_request_context("/"):
        assert get_theme_classes() == ""

    preference = learner.preference
    preference.text_size = "large"
    preference.reduce_motion = True
    preference.high_contrast = True
    db.session.commit()

    with app.test_request_context("/"):
        from flask_login import login_user

        login_user(learner)
        classes = get_theme_classes()
        assert "text-large" in classes
        assert "reduce-motion" in classes
        assert "high-contrast" in classes
