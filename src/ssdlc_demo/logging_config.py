import logging
from logging.config import dictConfig

from pythonjsonlogger import jsonlogger


def configure_logging(level: str | int = "INFO") -> None:
    """Configure JSON structured logging for the application.

    Args:
        level: Logging level name or numeric value.
    """
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": jsonlogger.JsonFormatter,
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "level": level,
                }
            },
            "root": {"handlers": ["default"], "level": level},
        }
    )

    # Reduce noisy third-party loggers if needed
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)
