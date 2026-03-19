from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()


def init_extensions(app) -> None:
    """
    Register Flask extensions in one place.

    Even if Stage 1 uses only CSRF, this pattern keeps the shell
    structured for SQLAlchemy, LoginManager, Migrate, etc. later.
    """
    csrf.init_app(app)