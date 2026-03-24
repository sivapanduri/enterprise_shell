from datetime import datetime, timezone

from app.extensions import db


class BrandingTheme(db.Model):
    __tablename__ = "branding_themes"

    id = db.Column(db.Integer, primary_key=True)

    theme_name = db.Column(db.String(120), nullable=False, default="Default Theme")
    app_name = db.Column(db.String(255), nullable=False, default="Enterprise Shell")
    app_tagline = db.Column(
        db.String(255),
        nullable=False,
        default="Reusable Flask foundation for enterprise business platforms.",
    )

    logo_path = db.Column(db.String(500), nullable=False, default="img/default-logo.svg")
    favicon_path = db.Column(db.String(500), nullable=True)

    primary_color = db.Column(db.String(20), nullable=False, default="#1f4b99")
    secondary_color = db.Column(db.String(20), nullable=False, default="#15356d")
    accent_color = db.Column(db.String(20), nullable=False, default="#eef4ff")

    sidebar_style = db.Column(db.String(50), nullable=False, default="dark")
    navbar_style = db.Column(db.String(50), nullable=False, default="light")

    login_title = db.Column(db.String(255), nullable=False, default="Sign in to Enterprise Shell")
    login_subtitle = db.Column(
        db.String(500),
        nullable=False,
        default="Use your account credentials to access the enterprise shell.",
    )

    public_hero_title = db.Column(
        db.String(255),
        nullable=False,
        default="Enterprise Shell",
    )
    public_hero_subtitle = db.Column(
        db.String(1000),
        nullable=False,
        default=(
            "A reusable Flask + Jinja foundation for enterprise business platforms, "
            "designed for maintainability, extensibility, auditability, and low-JavaScript workflows."
        ),
    )

    footer_text = db.Column(
        db.String(500),
        nullable=False,
        default="Enterprise Shell • Built for long-term maintainability",
    )

    is_active = db.Column(db.Boolean, nullable=False, default=True)

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
        return f"<BrandingTheme {self.theme_name}>"