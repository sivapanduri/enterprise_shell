from flask import render_template

from app.blueprints.audit import audit_bp
from app.models.audit import AuditTransaction
from app.security.decorators import permission_required


@audit_bp.get("/")
@permission_required("audit.view")
def list_transactions():
    transactions = (
        AuditTransaction.query.order_by(AuditTransaction.created_at.desc())
        .limit(100)
        .all()
    )
    return render_template("audit/list.html", transactions=transactions)


@audit_bp.get("/<int:tx_id>")
@permission_required("audit.view")
def transaction_detail(tx_id):
    tx = AuditTransaction.query.get_or_404(tx_id)
    return render_template("audit/detail.html", tx=tx)