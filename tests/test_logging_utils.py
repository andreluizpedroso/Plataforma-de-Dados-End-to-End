import logging

from ingestion.src.logging_utils import configure_logging


def test_configure_logging_sets_info_level_on_root_logger():
    root = logging.getLogger()
    previous_handlers = root.handlers[:]
    previous_level = root.level
    root.handlers = []

    try:
        configure_logging()
        assert root.level == logging.INFO
        assert len(root.handlers) == 1
    finally:
        root.handlers = previous_handlers
        root.level = previous_level
