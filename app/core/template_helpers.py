from datetime import datetime


def register_template_helpers(app) -> None:
    @app.template_filter("year")
    def year_filter(value):
        """
        Small reusable helper for footer/date rendering.
        """
        if isinstance(value, datetime):
            return value.year
        return value