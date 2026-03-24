from flask import Flask

from app.blueprints.auth import auth_bp
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.public import public_bp
from app.blueprints.roles import roles_bp
from app.blueprints.users import users_bp
from app.config import config_by_name
from app.core.context_processors import register_context_processors
from app.core.error_handlers import register_error_handlers
from app.core.template_helpers import register_template_helpers
from app.extensions import init_extensions
from app.logging_config import configure_logging
from app.permissions import PERMISSIONS


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    from app import models  # noqa: F401

    configure_logging(app)
    init_extensions(app)

    register_blueprints(app)
    register_context_processors(app)
    register_template_helpers(app)
    register_error_handlers(app)
    register_commands(app)

    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(roles_bp)


def register_commands(app: Flask) -> None:
    import click

    from app.extensions import db
    from app.models.rbac import Permission, Role, RolePermission, UserRole
    from app.models.user import User

    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.option("--username", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    @click.option("--first-name", default="")
    @click.option("--last-name", default="")
    def create_admin(email, username, password, first_name, last_name):
        email = email.strip().lower()
        username = username.strip()

        existing = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing:
            click.echo("A user with that email or username already exists.")
            return

        user = User(
            email=email,
            username=username,
            first_name=first_name.strip() or None,
            last_name=last_name.strip() or None,
            is_active=True,
            is_superadmin=True,
            must_change_password=False,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        click.echo(f"Admin user created: {email}")

    @app.cli.command("seed-permissions")
    def seed_permissions():
        created_count = 0

        for permission_name, module, description in PERMISSIONS:
            permission = Permission.query.filter_by(name=permission_name).first()
            if not permission:
                permission = Permission(
                    name=permission_name,
                    module=module,
                    description=description,
                    is_system_permission=True,
                )
                db.session.add(permission)
                created_count += 1
            else:
                permission.module = module
                permission.description = description
                permission.is_system_permission = True

        db.session.commit()
        click.echo(f"Permissions seeded. Created: {created_count}")

    @app.cli.command("bootstrap-rbac")
    @click.option(
        "--role-name",
        default="admin",
        show_default=True,
        help="System role name to create or update.",
    )
    def bootstrap_rbac(role_name):
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(
                name=role_name,
                label="Administrator",
                description="Baseline administrative role for shell management",
                is_system_role=True,
            )
            db.session.add(role)
            db.session.commit()

        permissions = Permission.query.all()
        existing_permission_ids = {
            rp.permission_id for rp in role.permissions
        }

        attached_count = 0
        for permission in permissions:
            if permission.id not in existing_permission_ids:
                db.session.add(
                    RolePermission(
                        role_id=role.id,
                        permission_id=permission.id,
                    )
                )
                attached_count += 1

        db.session.commit()
        click.echo(
            f"RBAC bootstrapped for role '{role.name}'. "
            f"Permissions attached: {attached_count}"
        )

    @app.cli.command("assign-role")
    @click.option("--email", prompt=True)
    @click.option("--role-name", prompt=True)
    def assign_role(email, role_name):
        email = email.strip().lower()
        role_name = role_name.strip()

        user = User.query.filter_by(email=email).first()
        if not user:
            click.echo("User not found.")
            return

        role = Role.query.filter_by(name=role_name).first()
        if not role:
            click.echo("Role not found.")
            return

        existing = UserRole.query.filter_by(user_id=user.id, role_id=role.id).first()
        if existing:
            click.echo("User already has that role.")
            return

        db.session.add(UserRole(user_id=user.id, role_id=role.id))
        db.session.commit()
        click.echo(f"Assigned role '{role.name}' to {user.email}")