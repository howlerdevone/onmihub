"""Structured logging configuration for omnihub."""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure root logger with standard formatting.

    Args:
        level: Logging level (default: logging.INFO)

    Returns:
        Configured root logger.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler with standard format
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
