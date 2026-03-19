import logging


def configure_logging(app) -> None:
    """
    Minimal structured logging foundation.

    This is intentionally simple for Stage 1, but centralizing logging now
    prevents scattered logging setup later as the shell grows.
    """
    if app.logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )