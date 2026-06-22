"""Download source datasets from KaggleHub into the local raw data folder."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

import kagglehub

from etl.config import get_settings
from etl.logging_config import configure_logging

LOGGER = logging.getLogger(__name__)

DATASETS = {
    "pokemon": "giorgiocarbone/complete-competitive-pokmon-datasets-may-2022",
    "earthquakes_chile": "nicolasgonzalezmunoz/earthquakes-on-chile",
    "yugioh": "hammadus/yugioh-full-card-database-index-august-1st-2025",
}


def copy_dataset_files(download_path: Path, target_dir: Path) -> None:
    """Copy downloaded files to the project raw folder."""

    target_dir.mkdir(parents=True, exist_ok=True)
    for source in download_path.rglob("*"):
        if source.is_file():
            destination = target_dir / source.relative_to(download_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)


def download_all() -> None:
    """Download all configured KaggleHub datasets."""

    settings = get_settings()
    settings.raw_dir.mkdir(parents=True, exist_ok=True)

    for dataset_name, dataset_ref in DATASETS.items():
        LOGGER.info("Downloading %s from %s", dataset_name, dataset_ref)
        downloaded_path = Path(kagglehub.dataset_download(dataset_ref))
        copy_dataset_files(downloaded_path, settings.raw_dir / dataset_name)
        LOGGER.info("Stored %s files in %s", dataset_name, settings.raw_dir / dataset_name)


if __name__ == "__main__":
    configure_logging(get_settings().log_level)
    download_all()
