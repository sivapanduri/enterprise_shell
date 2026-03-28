from app.extensions import db
from app.models.audit import AuditEntry, AuditTransaction
from app.models.audit_restore import AuditRestorationLog
from app.models.user import User
from app.models.rbac import Role


class RestoreService:
    """
    Handles preview + execution of restoration.
    """

    MODEL_MAP = {
        "users": User,
        "roles": Role,
    }

    @classmethod
    def preview_restore(cls, transaction_id: int):
        tx = AuditTransaction.query.get_or_404(transaction_id)

        preview = []

        for entry in reversed(tx.entries):
            action = cls._determine_reverse_action(entry)

            preview.append({
                "table": entry.table_name,
                "record_id": entry.record_id,
                "original_operation": entry.operation,
                "reverse_action": action,
                "before": entry.before_data,
                "after": entry.after_data,
                "conflict": cls._detect_conflict(entry),
            })

        return tx, preview

    @classmethod
    def execute_restore(cls, transaction_id: int, user_id: int):
        tx = AuditTransaction.query.get_or_404(transaction_id)

        results = []

        try:
            for entry in reversed(tx.entries):
                result = cls._apply_reverse(entry)
                results.append(result)

            log = AuditRestorationLog(
                transaction_id=transaction_id,
                restored_by_id=user_id,
                status="success",
                summary=results,
            )
            db.session.add(log)
            db.session.commit()

            return True, results

        except Exception as e:
            db.session.rollback()

            log = AuditRestorationLog(
                transaction_id=transaction_id,
                restored_by_id=user_id,
                status="failed",
                summary={"error": str(e)},
            )
            db.session.add(log)
            db.session.commit()

            return False, str(e)

    @classmethod
    def _determine_reverse_action(cls, entry: AuditEntry):
        if entry.operation == "INSERT":
            return "DELETE"
        elif entry.operation == "DELETE":
            return "INSERT"
        elif entry.operation == "UPDATE":
            return "REVERT"
        return "UNKNOWN"

    @classmethod
    def _detect_conflict(cls, entry: AuditEntry):
        model = cls.MODEL_MAP.get(entry.table_name)
        if not model:
            return False

        record = model.query.get(entry.record_id)

        if entry.operation == "INSERT":
            return record is None

        if entry.operation == "DELETE":
            return record is not None

        return False

    @classmethod
    def _apply_reverse(cls, entry: AuditEntry):
        model = cls.MODEL_MAP.get(entry.table_name)
        if not model:
            return {"status": "skipped", "reason": "unsupported table"}

        record = model.query.get(entry.record_id)

        if entry.operation == "INSERT":
            if record:
                db.session.delete(record)
                return {"action": "DELETE", "status": "ok"}

        elif entry.operation == "DELETE":
            data = entry.before_data
            obj = model(**data)
            db.session.add(obj)
            return {"action": "INSERT", "status": "ok"}

        elif entry.operation == "UPDATE":
            if record:
                for key, value in entry.before_data.items():
                    setattr(record, key, value)
                return {"action": "REVERT", "status": "ok"}

        return {"status": "noop"}