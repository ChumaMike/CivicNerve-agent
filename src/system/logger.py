import logging
import sys
from pythonjsonlogger import jsonlogger


def get_logger(name: str) -> logging.Logger:
    """Returns a JSON-formatted logger for structured log output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
