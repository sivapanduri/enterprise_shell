from datetime import datetime, timezone

from app.extensions import db


class AppSetting(db.Model):
    __tablename__ = "app_settings"
    __table_args__ = (
        db.UniqueConstraint("category", "key", name="uq_app_settings_category_key"),
    )

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), nullable=False, index=True)
    key = db.Column(db.String(120), nullable=False, index=True)

    value_text = db.Column(db.Text, nullable=True)
    value_type = db.Column(db.String(50), nullable=False, default="string")

    is_secret = db.Column(db.Boolean, nullable=False, default=False)
    is_system = db.Column(db.Boolean, nullable=False, default=False)

    description = db.Column(db.Text, nullable=True)

    updated_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    updated_by = db.relationship("User", foreign_keys=[updated_by_id])

    def __repr__(self) -> str:
        return f"<AppSetting {self.category}.{self.key}>"