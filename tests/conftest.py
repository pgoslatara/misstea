import logging
import os

import pytest


@pytest.fixture(autouse=True)
def reset_logging():
    logging.getLogger().handlers = []
    yield
    if "LOG_LEVEL" in os.environ:
        del os.environ["LOG_LEVEL"]
