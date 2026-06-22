"""Shared configuration helpers for local, API, dashboard and Docker runs."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    """Project settings loaded from environment variables."""

    project_name: str
    raw_dir: Path
    processed_dir: Path
    log_level: str
    api_host: str
    api_port: int


def get_settings() -> Settings:
    """Load environment variables and return normalized project settings."""

    load_dotenv(ROOT_DIR / ".env")

    raw_dir = Path(os.getenv("DATA_RAW_DIR", "data/raw"))
    processed_dir = Path(os.getenv("DATA_PROCESSED_DIR", "data/processed"))

    if not raw_dir.is_absolute():
        raw_dir = ROOT_DIR / raw_dir
    if not processed_dir.is_absolute():
        processed_dir = ROOT_DIR / processed_dir

    return Settings(
        project_name=os.getenv("PROJECT_NAME", "grupo-8-ciencias-de-datos"),
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        api_host=os.getenv("API_HOST", "0.0.0.0"),
        api_port=int(os.getenv("API_PORT", "8000")),
    )
