from datetime import datetime, timezone

from app.extensions import db


class AuditRestorationLog(db.Model):
    __tablename__ = "audit_restoration_logs"

    id = db.Column(db.BigInteger, primary_key=True)

    transaction_id = db.Column(db.BigInteger, nullable=False)
    restored_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    status = db.Column(db.String(50), nullable=False)  # success / failed / partial

    summary = db.Column(db.JSON, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    restored_by = db.relationship("User")

    def __repr__(self):
        return f"<AuditRestorationLog tx={self.transaction_id}>"