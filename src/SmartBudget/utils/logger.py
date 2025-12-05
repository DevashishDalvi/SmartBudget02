# File: src/smart_budget/utils/logger.py
import logging
import sys

from loguru import logger

from src.SmartBudget.config import settings


class InterceptHandler(logging.Handler):
    """
    Redirect standard logging messages to Loguru.
    This ensures libraries using standard 'logging' (like urllib3/pandas)
    appear in our Loguru formatting.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    """
    Configure the logging:
    1. Remove default handlers.
    2. Intercept standard library logging.
    3. Set format based on environment.
    """

    # Remove default logger
    # (which prints to stderr by default with default format)
    logger.remove()

    # Define the format.
    # In local dev: Human readable with colors.
    # In prod: structured or simplified (we keep human readable for this MVP).
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # Add the sink (Destination)
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format=log_format,
        colorize=True,  # Docker logs support colors, looks nice
        backtrace=True,
        # Show variables in exception traces
        # (Security risk in strict prod, ok for MVP)
        diagnose=True,
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Mute noisy libraries if needed (optional)
    # logging.getLogger("urllib3").setLevel(logging.WARNING)

    logger.info(f"Logging configured. Level: {settings.LOG_LEVEL}")


# Expose the logger for easy import
__all__ = ["logger", "setup_logging"]
