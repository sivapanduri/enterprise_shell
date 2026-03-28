from flask import Blueprint

audit_restore_bp = Blueprint(
    "audit_restore",
    __name__,
    url_prefix="/audit",
)

from app.blueprints.audit_restore import routes