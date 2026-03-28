from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app.blueprints.audit_restore import audit_restore_bp
from app.security.decorators import permission_required
from app.services.restore_service import RestoreService


@audit_restore_bp.get("/<int:tx_id>/restore/preview")
@permission_required("audit.restore_preview")
def preview(tx_id: int):
    tx, preview = RestoreService.preview_restore(tx_id)
    has_conflicts = any(item.get("conflict") for item in preview)

    return render_template(
        "audit/restore_preview.html",
        tx=tx,
        preview=preview,
        has_conflicts=has_conflicts,
    )


@audit_restore_bp.post("/<int:tx_id>/restore/execute")
@permission_required("audit.restore_execute")
def execute(tx_id: int):
    if not current_user.is_superadmin:
        flash("Only a super-admin can execute restoration.", "danger")
        return redirect(url_for("audit_restore.preview", tx_id=tx_id))

    tx, preview = RestoreService.preview_restore(tx_id)
    has_conflicts = any(item.get("conflict") for item in preview)

    if has_conflicts:
        flash("Restore execution is blocked because conflicts were detected.", "danger")
        return redirect(url_for("audit_restore.preview", tx_id=tx_id))

    success, result = RestoreService.execute_restore(tx_id, current_user.id)

    return render_template(
        "audit/restore_result.html",
        tx=tx,
        success=success,
        result=result,
    )