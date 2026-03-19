import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    APP_ENV = os.getenv("APP_ENV", "development")

    # Database is not used in Stage 1 yet, but keeping the setting now
    # avoids restructuring later.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/enterprise_shell",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Shell branding defaults for Stage 1.
    APP_NAME = os.getenv("APP_NAME", "Enterprise Shell")
    APP_TAGLINE = os.getenv(
        "APP_TAGLINE",
        "Reusable Flask foundation for enterprise business platforms.",
    )
    APP_LOGO = os.getenv("APP_LOGO", "img/default-logo.svg")
    APP_FOOTER_TEXT = os.getenv(
        "APP_FOOTER_TEXT",
        "Enterprise Shell • Built for long-term maintainability",
    )

    COMPANY_NAME = os.getenv("COMPANY_NAME", "Your Organization")
    SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@example.com")

    # Basic UI defaults. In later stages this will be resolved
    # through settings/branding services and database values.
    THEME_PRIMARY = os.getenv("THEME_PRIMARY", "#1f4b99")
    THEME_SECONDARY = os.getenv("THEME_SECONDARY", "#15356d")
    THEME_ACCENT = os.getenv("THEME_ACCENT", "#eef4ff")

    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}