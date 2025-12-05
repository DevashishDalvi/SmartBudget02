from loguru import logger


def test_dummy() -> None:
    logger.info("test 01...")
    assert True


def test_math() -> None:
    logger.info("test 02...")
    _ = 1 + 1
    assert _ == 2
