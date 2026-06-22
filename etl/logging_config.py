"""Logging setup used by scripts and services."""

from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure a concise console logger."""

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
