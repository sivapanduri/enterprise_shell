from flask import render_template
from flask_login import login_required

from app.blueprints.dashboard import dashboard_bp
from app.models.user import User


@dashboard_bp.get("/")
@login_required
def index():
    stats = {
        "total_users": User.query.count(),
        "active_users": User.query.filter_by(is_active=True).count(),
    }
    return render_template("dashboard/index.html", stats=stats)