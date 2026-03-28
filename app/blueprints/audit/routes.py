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
def transaction_detail(tx_id: int):
    tx = AuditTransaction.query.get_or_404(tx_id)

    entry_summaries = []
    for entry in tx.entries:
        before_keys = sorted(entry.before_data.keys()) if isinstance(entry.before_data, dict) else []
        after_keys = sorted(entry.after_data.keys()) if isinstance(entry.after_data, dict) else []

        changed_keys = sorted(set(before_keys) | set(after_keys))
        entry_summaries.append(
            {
                "entry": entry,
                "changed_keys": changed_keys,
            }
        )

    return render_template(
        "audit/detail.html",
        tx=tx,
        entry_summaries=entry_summaries,
    )