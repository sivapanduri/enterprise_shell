from flask import Blueprint


branding_bp = Blueprint("branding", __name__, url_prefix="/branding")


from app.blueprints.branding import routes  # noqa: E402,F401