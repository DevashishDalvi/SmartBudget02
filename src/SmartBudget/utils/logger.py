# File: src/smart_budget/utils/logger.py
import logging
import sys
from datetime import date

from loguru import logger

from SmartBudget.config import settings


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
        frame = logging.currentframe()
        depth = 2
        while frame is not None:  # pyre-ignore[7]
            if frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back  # pyre-ignore[7]
                depth += 1
            else:
                break

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

    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format=log_format,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        f"logs/log{date.today().strftime('%y%m%d')}.json",
        level=settings.LOG_LEVEL,
        format=log_format,
        serialize=True,
        rotation="10 MB",
        backtrace=True,
        diagnose=True,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.info(f"Logging configured. Level: {settings.LOG_LEVEL}")


__all__ = ["logger", "setup_logging"]
