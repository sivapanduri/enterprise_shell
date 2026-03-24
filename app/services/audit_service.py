from flask import request
from flask_login import current_user

from app.extensions import db
from app.models.audit import AuditEntry, AuditTransaction


class AuditService:
    """
    Central audit service.

    Responsible for:
    - starting transactions
    - recording entries
    - committing grouped changes
    """

    @staticmethod
    def start_transaction(action: str, description: str = None):
        tx = AuditTransaction(
            actor_id=current_user.id if current_user.is_authenticated else None,
            action=action,
            description=description,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
        )
        db.session.add(tx)
        db.session.flush()
        return tx

    @staticmethod
    def add_entry(
        transaction: AuditTransaction,
        *,
        table_name: str,
        record_id: str,
        operation: str,
        before_data=None,
        after_data=None,
    ):
        entry = AuditEntry(
            transaction_id=transaction.id,
            table_name=table_name,
            record_id=str(record_id),
            operation=operation,
            before_data=before_data,
            after_data=after_data,
        )
        db.session.add(entry)

    @staticmethod
    def commit():
        db.session.commit()