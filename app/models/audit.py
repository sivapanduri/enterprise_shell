from datetime import datetime, timezone

from app.extensions import db


class AuditTransaction(db.Model):
    __tablename__ = "audit_transactions"

    id = db.Column(db.BigInteger, primary_key=True)

    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # e.g. "user.create"
    description = db.Column(db.String(500), nullable=True)

    ip_address = db.Column(db.String(100), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    actor = db.relationship("User")

    entries = db.relationship(
        "AuditEntry",
        backref="transaction",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self):
        return f"<AuditTransaction {self.id} {self.action}>"

class AuditEntry(db.Model):
    __tablename__ = "audit_entries"

    id = db.Column(db.BigInteger, primary_key=True)

    transaction_id = db.Column(
        db.BigInteger,
        db.ForeignKey("audit_transactions.id"),
        nullable=False,
        index=True,
    )

    table_name = db.Column(db.String(120), nullable=False)
    record_id = db.Column(db.String(120), nullable=True)

    operation = db.Column(db.String(20), nullable=False)
    # INSERT / UPDATE / DELETE

    before_data = db.Column(db.JSON, nullable=True)
    after_data = db.Column(db.JSON, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<AuditEntry {self.table_name} {self.operation}>"