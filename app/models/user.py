from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)

    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_superadmin = db.Column(db.Boolean, nullable=False, default=False)
    must_change_password = db.Column(db.Boolean, nullable=False, default=True)

    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)
    last_login_ip = db.Column(db.String(64), nullable=True)

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

    roles = db.relationship(
        "UserRole",
        foreign_keys="UserRole.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    @property
    def display_name(self) -> str:
        full_name = " ".join(
            part for part in [self.first_name, self.last_name] if part
        ).strip()
        return full_name or self.username

    def get_role_names(self) -> set[str]:
        return {user_role.role.name for user_role in self.roles if user_role.role}

    def get_permission_names(self) -> set[str]:
        permission_names = set()

        for user_role in self.roles:
            if not user_role.role:
                continue

            for role_permission in user_role.role.permissions:
                if role_permission.permission:
                    permission_names.add(role_permission.permission.name)

        return permission_names

    def has_permission(self, permission_name: str) -> bool:
        if self.is_superadmin:
            return True

        return permission_name in self.get_permission_names()

    def __repr__(self) -> str:
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))