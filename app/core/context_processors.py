from flask import current_app


def register_context_processors(app) -> None:
    @app.context_processor
    def inject_shell_context():
        """
        Expose shell-wide template context from one controlled place.

        Later this will be replaced or enriched by branding and settings services.
        """
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
            }
        }