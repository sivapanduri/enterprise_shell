from flask import render_template

from app.blueprints.dashboard import dashboard_bp
from app.models.rbac import Permission, Role
from app.models.user import User
from app.security.decorators import permission_required


@dashboard_bp.get("/")
@permission_required("dashboard.view")
def index():
    stats = {
        "total_users": User.query.count(),
        "active_users": User.query.filter_by(is_active=True).count(),
        "total_roles": Role.query.count(),
        "total_permissions": Permission.query.count(),
    }
    return render_template("dashboard/index.html", stats=stats)