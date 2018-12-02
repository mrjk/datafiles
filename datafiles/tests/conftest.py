from shutil import get_terminal_size

import log
import pytest


@pytest.fixture
def logbreak():
    def _():
        width = get_terminal_size().columns - 40
        line = '-' * width
        log.info(line)

    return _