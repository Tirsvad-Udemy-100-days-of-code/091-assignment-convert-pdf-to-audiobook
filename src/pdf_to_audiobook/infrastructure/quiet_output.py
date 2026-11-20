"""@brief Hide the console output of the speech library while it works."""

import contextlib
import io
import logging
import os
from collections.abc import Iterator

from pdf_to_audiobook.constants import QUIET_ENVIRONMENT, QUIET_LOGGER_NAMES


@contextlib.contextmanager
def quiet_output(enabled: bool) -> Iterator[None]:
    """!@brief Discard stdout, stderr, library logs and progress bars in a block.

    Streams, logger levels and environment variables are restored when the block
    ends, also after an exception; the exception itself is not touched.

    @param enabled False makes the block run unchanged.
    @return A context manager.
    """
    if not enabled:
        yield
        return
    saved_levels = {name: logging.getLogger(name).level for name in QUIET_LOGGER_NAMES}
    saved_environment = {name: os.environ.get(name) for name in QUIET_ENVIRONMENT}
    for name in QUIET_LOGGER_NAMES:
        logging.getLogger(name).setLevel(logging.CRITICAL + 1)
    os.environ.update(QUIET_ENVIRONMENT)
    try:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            yield
    finally:
        for name, level in saved_levels.items():
            logging.getLogger(name).setLevel(level)
        _restore_environment(saved_environment)


def _restore_environment(saved: dict[str, str | None]) -> None:
    """!@brief Put environment variables back to their saved values.

    @param saved Variable name to the old value, or None if it was not set.
    @return Nothing.
    """
    for name, value in saved.items():
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value
