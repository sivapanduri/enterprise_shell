from datetime import datetime, timezone

from flask import current_app, render_template

from app.blueprints.public import public_bp


@public_bp.get("/")
def home():
    return render_template("public/home.html")


@public_bp.get("/about")
def about():
    return render_template("public/about.html")


@public_bp.get("/status")
def status():
    """
    Human-friendly status page for quick checks during development
    and early deployment smoke testing.
    """
    status_data = {
        "app_name": current_app.config["APP_NAME"],
        "environment": current_app.config["APP_ENV"],
        "utc_time": datetime.now(timezone.utc),
        "status": "OK",
    }
    return render_template("public/status.html", status_data=status_data)