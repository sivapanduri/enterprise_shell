from flask import current_app, request, url_for
from flask_login import current_user

from app.menu import get_admin_menu


def _item_is_active(item, endpoint: str | None) -> bool:
    if item.endpoint and item.endpoint == endpoint:
        return True

    for child in item.children:
        if child.endpoint == endpoint:
            return True

    return False


def register_context_processors(app) -> None:
    @app.context_processor
    def inject_shell_context():
        current_endpoint = request.endpoint
        admin_menu = get_admin_menu()

        return {
            "branding": {
                "app_name": current_app.config["APP_NAME"],
                "app_tagline": current_app.config["APP_TAGLINE"],
                "app_logo": current_app.config["APP_LOGO"],
                "footer_text": current_app.config["APP_FOOTER_TEXT"],
                "company_name": current_app.config["COMPANY_NAME"],
                "support_email": current_app.config["SUPPORT_EMAIL"],
                "theme_primary": current_app.config["THEME_PRIMARY"],
                "theme_secondary": current_app.config["THEME_SECONDARY"],
                "theme_accent": current_app.config["THEME_ACCENT"],
            },
            "current_user": current_user,
            "admin_menu": admin_menu,
            "is_menu_item_active": lambda item: _item_is_active(item, current_endpoint),
            "shell_links": {
                "dashboard": url_for("dashboard.index"),
                "public_home": url_for("public.home"),
                "logout": url_for("auth.logout"),
            },
        }