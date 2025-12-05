import logging

from loguru import logger

from src.SmartBudget.utils.logger import setup_logging

setup_logging()


def main() -> None:
    logger.info("Hello from smartbudget02!")


if __name__ == "__main__":
    main()
    std_logger = logging.getLogger("some_lib")
    std_logger.warning("some_lib warning!!")
