import logging
import os

from misstea import logger


def test_custom_formatter():
    formatter = logger.CustomFormatter(logging.INFO)
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    formatted_message = formatter.format(record)
    assert "Test message" in formatted_message


def test_configure_console_logging_default():
    logger.configure_console_logging(verbosity=0)
    log = logging.getLogger()
    assert any(
        isinstance(h, logging.StreamHandler) and h.level == logging.INFO
        for h in log.handlers
    )


def test_configure_console_logging_verbose():
    logger.configure_console_logging(verbosity=1)
    log = logging.getLogger()
    assert any(
        isinstance(h, logging.StreamHandler) and h.level == logging.DEBUG
        for h in log.handlers
    )


def test_configure_console_logging_env_var():
    os.environ["LOG_LEVEL"] = "DEBUG"
    logger.configure_console_logging(verbosity=0)
    log = logging.getLogger()
    assert any(
        isinstance(h, logging.StreamHandler) and h.level == logging.DEBUG
        for h in log.handlers
    )
