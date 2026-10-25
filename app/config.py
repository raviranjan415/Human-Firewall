"""Application configuration.

Values are read from environment variables (see `.env.example`).
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(value: str | None, default: int) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


class BaseConfig:
    """Configuration shared by every environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-insecure-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'cyberquest.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # --- Security ---------------------------------------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _as_bool(os.environ.get("SESSION_COOKIE_SECURE"), False)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = _as_bool(os.environ.get("REMEMBER_COOKIE_SECURE"), False)
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=_as_int(os.environ.get("PERMANENT_SESSION_LIFETIME_MINUTES"), 120)
    )
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Secure HTTP headers applied by an after_request hook.
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    # --- Rate limiting ----------------------------------------------------
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_DEFAULT = "600 per hour"
    LOGIN_RATE_LIMIT = os.environ.get("LOGIN_RATE_LIMIT", "10 per minute")

    # --- Uploads ----------------------------------------------------------
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
    ALLOWED_UPLOAD_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg", "pdf"}

    # --- Gamification defaults (administrator-configurable) ---------------
    DEFAULT_LOCALE = "en"
    SUPPORTED_LOCALES = ("en", "hi")
    CERTIFICATE_PASS_SCORE = _as_int(os.environ.get("CERTIFICATE_PASS_SCORE"), 80)
    XP_REWARDS = {
        "video_lesson": _as_int(os.environ.get("XP_VIDEO_LESSON"), 20),
        "comic": _as_int(os.environ.get("XP_COMIC"), 15),
        "lab_basic": _as_int(os.environ.get("XP_LAB_BASIC"), 30),
        "lab_intermediate": _as_int(os.environ.get("XP_LAB_INTERMEDIATE"), 50),
        "lab_advanced": _as_int(os.environ.get("XP_LAB_ADVANCED"), 75),
        "lab_capstone": _as_int(os.environ.get("XP_LAB_CAPSTONE"), 150),
        "daily_challenge": _as_int(os.environ.get("XP_DAILY_CHALLENGE"), 25),
        "perfect_bonus": _as_int(os.environ.get("XP_PERFECT_BONUS"), 10),
        "game": _as_int(os.environ.get("XP_GAME"), 25),
    }
    LAB_LEVEL_XP = {
        "basic": "lab_basic",
        "intermediate": "lab_intermediate",
        "advanced": "lab_advanced",
        "capstone": "lab_capstone",
    }

    # --- Bootstrap accounts ----------------------------------------------
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@cyberquest.example")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
    CREATE_DEMO_ACCOUNTS = _as_bool(os.environ.get("CREATE_DEMO_ACCOUNTS"), True)
    DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "Demo@12345")

    # --- News ingestion ---------------------------------------------------
    NEWS_INGEST_ENABLED = _as_bool(os.environ.get("NEWS_INGEST_ENABLED"), True)
    NEWS_INGEST_INTERVAL_HOURS = _as_int(os.environ.get("NEWS_INGEST_INTERVAL_HOURS"), 6)
    NEWS_MAX_ITEMS_PER_SOURCE = _as_int(os.environ.get("NEWS_MAX_ITEMS_PER_SOURCE"), 15)

    # --- i18n -------------------------------------------------------------
    BABEL_DEFAULT_LOCALE = "en"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # in-memory
    CREATE_DEMO_ACCOUNTS = False
    ADMIN_PASSWORD = "Admin@150305"
    SERVER_NAME = "localhost"


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # Demo accounts must never exist in production.
    CREATE_DEMO_ACCOUNTS = False


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name: str | None = None):
    """Return the configuration class for the given environment name."""
    name = (name or os.environ.get("FLASK_ENV") or "development").lower()
    return CONFIG_MAP.get(name, DevelopmentConfig)
