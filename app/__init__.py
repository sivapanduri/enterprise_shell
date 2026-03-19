from flask import Flask

from app.blueprints.auth import auth_bp
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.public import public_bp
from app.config import config_by_name
from app.core.context_processors import register_context_processors
from app.core.error_handlers import register_error_handlers
from app.core.template_helpers import register_template_helpers
from app.extensions import init_extensions
from app.logging_config import configure_logging


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


def register_commands(app: Flask) -> None:
    import click

    from app.extensions import db
    from app.models.user import User

    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.option("--username", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    @click.option("--first-name", default="")
    @click.option("--last-name", default="")
    def create_admin(email, username, password, first_name, last_name):
        """
        Create the first administrative user from CLI.

        This avoids unsafe bootstrap hacks through public routes.
        """
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