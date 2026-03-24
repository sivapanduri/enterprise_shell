from __future__ import annotations

from typing import Any

from app.extensions import db
from app.models.settings import AppSetting


class SettingsService:
    """
    Central service for reading and writing application settings.

    Templates and route handlers should prefer this service over scattered
    direct database access so the shell can evolve settings behavior cleanly.
    """

    GENERAL_DEFAULTS = {
        "app_display_name": "Enterprise Shell",
        "app_tagline": "Reusable Flask foundation for enterprise business platforms.",
        "company_name": "Your Organization",
        "support_email": "support@example.com",
        "footer_text": "Enterprise Shell • Built for long-term maintainability",
    }

    SECURITY_DEFAULTS = {
        "password_min_length": 8,
        "session_timeout_minutes": 60,
        "remember_me_enabled": True,
        "force_password_change_on_first_login": True,
    }

    @classmethod
    def get(cls, category: str, key: str, default: Any = None) -> Any:
        setting = AppSetting.query.filter_by(category=category, key=key).first()
        if not setting or setting.value_text is None:
            if default is not None:
                return default
            return cls._default_value(category, key)

        return cls._deserialize(setting.value_text, setting.value_type)

    @classmethod
    def set(
        cls,
        *,
        category: str,
        key: str,
        value: Any,
        value_type: str = "string",
        description: str | None = None,
        is_secret: bool = False,
        is_system: bool = False,
        updated_by_id: int | None = None,
    ) -> AppSetting:
        setting = AppSetting.query.filter_by(category=category, key=key).first()
        if not setting:
            setting = AppSetting(category=category, key=key)
            db.session.add(setting)

        setting.value_text = cls._serialize(value, value_type)
        setting.value_type = value_type
        setting.description = description
        setting.is_secret = is_secret
        setting.is_system = is_system
        setting.updated_by_id = updated_by_id

        db.session.flush()
        return setting

    @classmethod
    def save_general_settings(cls, data: dict[str, Any], updated_by_id: int | None = None) -> None:
        cls.set(
            category="general",
            key="app_display_name",
            value=data["app_display_name"],
            value_type="string",
            description="Primary application display name",
            updated_by_id=updated_by_id,
        )
        cls.set(
            category="general",
            key="app_tagline",
            value=data["app_tagline"],
            value_type="string",
            description="Application tagline shown in shell surfaces",
            updated_by_id=updated_by_id,
        )
        cls.set(
            category="general",
            key="company_name",
            value=data["company_name"],
            value_type="string",
            description="Owning organization name",
            updated_by_id=updated_by_id,
        )
        cls.set(
            category="general",
            key="support_email",
            value=data["support_email"],
            value_type="string",
            description="Primary support email address",
            updated_by_id=updated_by_id,
        )
        cls.set(
            category="general",
            key="footer_text",
            value=data["footer_text"],
            value_type="string",
            description="Footer display text",
            updated_by_id=updated_by_id,
        )
        db.session.commit()

    @classmethod
    def save_security_settings(cls, data: dict[str, Any], updated_by_id: int | None = None) -> None:
        cls.set(
            category="security",
            key="password_min_length",
            value=data["password_min_length"],
            value_type="int",
            description="Minimum allowed password length",
            updated_by_id=updated_by_id,
        )
        cls.set(
            category="security",
            key="session_timeout_minutes",
            value=data["session_timeout_minutes"],
            value_type="int",
            description="Configured session timeout in minutes",
            updated_by_id=updated_by_id,
        )
        cls.set(
            category="security",
            key="remember_me_enabled",
            value=data["remember_me_enabled"],
            value_type="bool",
            description="Whether remember-me logins are enabled",
            updated_by_id=updated_by_id,
        )
        cls.set(
            category="security",
            key="force_password_change_on_first_login",
            value=data["force_password_change_on_first_login"],
            value_type="bool",
            description="Require password change for first login users",
            updated_by_id=updated_by_id,
        )
        db.session.commit()

    @classmethod
    def get_general_settings(cls) -> dict[str, Any]:
        return {
            "app_display_name": cls.get("general", "app_display_name"),
            "app_tagline": cls.get("general", "app_tagline"),
            "company_name": cls.get("general", "company_name"),
            "support_email": cls.get("general", "support_email"),
            "footer_text": cls.get("general", "footer_text"),
        }

    @classmethod
    def get_security_settings(cls) -> dict[str, Any]:
        return {
            "password_min_length": cls.get("security", "password_min_length"),
            "session_timeout_minutes": cls.get("security", "session_timeout_minutes"),
            "remember_me_enabled": cls.get("security", "remember_me_enabled"),
            "force_password_change_on_first_login": cls.get("security", "force_password_change_on_first_login"),
        }

    @classmethod
    def _default_value(cls, category: str, key: str) -> Any:
        if category == "general":
            return cls.GENERAL_DEFAULTS.get(key)
        if category == "security":
            return cls.SECURITY_DEFAULTS.get(key)
        return None

    @staticmethod
    def _serialize(value: Any, value_type: str) -> str:
        if value_type == "bool":
            return "true" if bool(value) else "false"
        return str(value)

    @staticmethod
    def _deserialize(value: str, value_type: str) -> Any:
        if value_type == "int":
            return int(value)
        if value_type == "bool":
            return value.lower() in {"true", "1", "yes", "on"}
        return value