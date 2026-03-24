from __future__ import annotations

from typing import Any

from app.extensions import db
from app.models.branding import BrandingTheme
from app.services.settings_service import SettingsService


class BrandingService:
    """
    Central resolver for active branding.

    The shell should read brand values from here instead of scattering theme logic
    across templates and route handlers.
    """

    DEFAULTS = {
        "theme_name": "Default Theme",
        "app_name": "Enterprise Shell",
        "app_tagline": "Reusable Flask foundation for enterprise business platforms.",
        "logo_path": "img/default-logo.svg",
        "favicon_path": "",
        "primary_color": "#1f4b99",
        "secondary_color": "#15356d",
        "accent_color": "#eef4ff",
        "sidebar_style": "dark",
        "navbar_style": "light",
        "login_title": "Sign in to Enterprise Shell",
        "login_subtitle": "Use your account credentials to access the enterprise shell.",
        "public_hero_title": "Enterprise Shell",
        "public_hero_subtitle": (
            "A reusable Flask + Jinja foundation for enterprise business platforms, "
            "designed for maintainability, extensibility, auditability, and low-JavaScript workflows."
        ),
        "footer_text": "Enterprise Shell • Built for long-term maintainability",
    }

    @classmethod
    def get_active_theme(cls) -> BrandingTheme | None:
        return BrandingTheme.query.filter_by(is_active=True).order_by(BrandingTheme.id.asc()).first()

    @classmethod
    def get_effective_branding(cls) -> dict[str, Any]:
        general_settings = SettingsService.get_general_settings()
        theme = cls.get_active_theme()

        branding = dict(cls.DEFAULTS)

        branding["app_name"] = general_settings.get("app_display_name") or branding["app_name"]
        branding["app_tagline"] = general_settings.get("app_tagline") or branding["app_tagline"]
        branding["footer_text"] = general_settings.get("footer_text") or branding["footer_text"]
        branding["company_name"] = general_settings.get("company_name") or "Your Organization"
        branding["support_email"] = general_settings.get("support_email") or "support@example.com"

        if theme:
            branding.update(
                {
                    "theme_name": theme.theme_name,
                    "app_name": theme.app_name or branding["app_name"],
                    "app_tagline": theme.app_tagline or branding["app_tagline"],
                    "logo_path": theme.logo_path or branding["logo_path"],
                    "favicon_path": theme.favicon_path or branding["favicon_path"],
                    "primary_color": theme.primary_color or branding["primary_color"],
                    "secondary_color": theme.secondary_color or branding["secondary_color"],
                    "accent_color": theme.accent_color or branding["accent_color"],
                    "sidebar_style": theme.sidebar_style or branding["sidebar_style"],
                    "navbar_style": theme.navbar_style or branding["navbar_style"],
                    "login_title": theme.login_title or branding["login_title"],
                    "login_subtitle": theme.login_subtitle or branding["login_subtitle"],
                    "public_hero_title": theme.public_hero_title or branding["public_hero_title"],
                    "public_hero_subtitle": theme.public_hero_subtitle or branding["public_hero_subtitle"],
                    "footer_text": theme.footer_text or branding["footer_text"],
                }
            )

        return branding

    @classmethod
    def get_or_create_active_theme(cls) -> BrandingTheme:
        theme = cls.get_active_theme()
        if theme:
            return theme

        theme = BrandingTheme(
            theme_name=cls.DEFAULTS["theme_name"],
            app_name=cls.DEFAULTS["app_name"],
            app_tagline=cls.DEFAULTS["app_tagline"],
            logo_path=cls.DEFAULTS["logo_path"],
            favicon_path=cls.DEFAULTS["favicon_path"],
            primary_color=cls.DEFAULTS["primary_color"],
            secondary_color=cls.DEFAULTS["secondary_color"],
            accent_color=cls.DEFAULTS["accent_color"],
            sidebar_style=cls.DEFAULTS["sidebar_style"],
            navbar_style=cls.DEFAULTS["navbar_style"],
            login_title=cls.DEFAULTS["login_title"],
            login_subtitle=cls.DEFAULTS["login_subtitle"],
            public_hero_title=cls.DEFAULTS["public_hero_title"],
            public_hero_subtitle=cls.DEFAULTS["public_hero_subtitle"],
            footer_text=cls.DEFAULTS["footer_text"],
            is_active=True,
        )
        db.session.add(theme)
        db.session.commit()
        return theme

    @classmethod
    def save_theme_settings(cls, data: dict[str, Any], updated_by_id: int | None = None) -> BrandingTheme:
        theme = cls.get_or_create_active_theme()
        theme.theme_name = data["theme_name"]
        theme.app_name = data["app_name"]
        theme.app_tagline = data["app_tagline"]
        theme.logo_path = data["logo_path"]
        theme.favicon_path = data["favicon_path"]
        theme.primary_color = data["primary_color"]
        theme.secondary_color = data["secondary_color"]
        theme.accent_color = data["accent_color"]
        theme.sidebar_style = data["sidebar_style"]
        theme.navbar_style = data["navbar_style"]
        theme.footer_text = data["footer_text"]
        theme.updated_by_id = updated_by_id
        db.session.commit()
        return theme

    @classmethod
    def save_login_branding(cls, data: dict[str, Any], updated_by_id: int | None = None) -> BrandingTheme:
        theme = cls.get_or_create_active_theme()
        theme.login_title = data["login_title"]
        theme.login_subtitle = data["login_subtitle"]
        theme.updated_by_id = updated_by_id
        db.session.commit()
        return theme

    @classmethod
    def save_public_branding(cls, data: dict[str, Any], updated_by_id: int | None = None) -> BrandingTheme:
        theme = cls.get_or_create_active_theme()
        theme.public_hero_title = data["public_hero_title"]
        theme.public_hero_subtitle = data["public_hero_subtitle"]
        theme.updated_by_id = updated_by_id
        db.session.commit()
        return theme