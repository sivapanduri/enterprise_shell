from flask import Flask

from app.blueprints.public import public_bp
from app.config import config_by_name
from app.core.context_processors import register_context_processors
from app.core.error_handlers import register_error_handlers
from app.core.template_helpers import register_template_helpers
from app.extensions import init_extensions
from app.logging_config import configure_logging


def create_app(config_name: str = "development") -> Flask:
    """
    Application factory for the reusable enterprise shell.

    Using an app factory from the start makes it much easier to:
    - swap environments cleanly
    - test the app in isolation
    - extend the shell for future products
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    configure_logging(app)
    init_extensions(app)

    register_blueprints(app)
    register_context_processors(app)
    register_template_helpers(app)
    register_error_handlers(app)

    return app


def register_blueprints(app: Flask) -> None:
    """
    Keep blueprint registration centralized so future modules
    can be added in a predictable way.
    """
    app.register_blueprint(public_bp)