from flask import request, url_for
from flask_login import current_user

from app.menu import get_admin_menu
from app.services.branding_service import BrandingService


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
        branding = BrandingService.get_effective_branding()

        return {
            "branding": branding,
            "current_user": current_user,
            "admin_menu": admin_menu,
            "is_menu_item_active": lambda item: _item_is_active(item, current_endpoint),
            "shell_links": {
                "dashboard": url_for("dashboard.index"),
                "public_home": url_for("public.home"),
                "logout": url_for("auth.logout"),
            },
        }