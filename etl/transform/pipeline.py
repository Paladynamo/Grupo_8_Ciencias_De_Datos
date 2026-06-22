"""End-to-end transformation pipeline."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from etl.config import get_settings
from etl.logging_config import configure_logging
from etl.transform.common import clean_dataframe, parse_currency_series, parse_percent_series, read_tabular_file
from etl.validation import validate_dataframe

LOGGER = logging.getLogger(__name__)
SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def discover_source_files(raw_dir: Path) -> list[Path]:
    """Find supported raw files recursively."""

    return sorted(
        path
        for path in raw_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def transform_file(path: Path, raw_dir: Path) -> pd.DataFrame:
    """Read, clean and validate a single raw file."""

    source_name = path.relative_to(raw_dir).parts[0]
    df = read_tabular_file(path)
    cleaned = clean_dataframe(df, source_name=source_name, source_file=path)
    cleaned = apply_source_specific_transforms(cleaned, source_name=source_name)
    validate_dataframe(cleaned, dataset_name=source_name)
    return cleaned


def apply_source_specific_transforms(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """Apply conservative type conversions for each project module."""

    transformed = df.copy()

    if source_name == "earthquakes_chile":
        if "date_utc" in transformed.columns:
            transformed["date_utc"] = pd.to_datetime(transformed["date_utc"], errors="coerce", utc=True)
            transformed["year"] = transformed["date_utc"].dt.year
            transformed["month"] = transformed["date_utc"].dt.month
        for column in ["latitude", "longitude", "depth", "magnitude"]:
            if column in transformed.columns:
                transformed[column] = pd.to_numeric(transformed[column], errors="coerce")

    if source_name == "pokemon":
        for column in transformed.columns:
            if "percentage" in column or "percent" in column:
                transformed[f"{column}_numeric"] = parse_percent_series(transformed[column])
        numeric_columns = [
            "id",
            "generation",
            "total",
            "hp",
            "attack",
            "defense",
            "sp_atk",
            "sp_def",
            "speed",
            "monthly_usage_k",
            "monthly_rank",
            "power",
            "pp",
            "prob",
        ]
        for column in numeric_columns:
            if column in transformed.columns:
                transformed[column] = pd.to_numeric(transformed[column], errors="coerce")

    if source_name == "yugioh":
        if "price" in transformed.columns:
            transformed["price_numeric"] = parse_currency_series(transformed["price"])
        if "set_release" in transformed.columns:
            transformed["set_release"] = pd.to_datetime(transformed["set_release"], errors="coerce")
            transformed["release_year"] = transformed["set_release"].dt.year
        for column in ["attack", "defense", "rank"]:
            if column in transformed.columns:
                transformed[column] = pd.to_numeric(transformed[column], errors="coerce")

    return transformed


def run_pipeline() -> list[Path]:
    """Transform every raw tabular file and persist one Parquet file per source file."""

    settings = get_settings()
    settings.processed_dir.mkdir(parents=True, exist_ok=True)

    source_files = discover_source_files(settings.raw_dir)
    if not source_files:
        raise FileNotFoundError(
            f"No CSV/Excel files found in {settings.raw_dir}. Run the Kaggle download step first."
        )

    output_files: list[Path] = []
    for source_file in source_files:
        LOGGER.info("Transforming %s", source_file)
        transformed = transform_file(source_file, settings.raw_dir)
        source_name = source_file.relative_to(settings.raw_dir).parts[0]
        output_dir = settings.processed_dir / source_name
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{source_file.stem}.parquet"
        transformed.to_parquet(output_file, index=False)
        output_files.append(output_file)
        LOGGER.info("Wrote %s rows to %s", len(transformed), output_file)

    return output_files


if __name__ == "__main__":
    configure_logging(get_settings().log_level)
    run_pipeline()
