"""Lightweight validation rules for transformed data."""

from __future__ import annotations

import pandas as pd


class DataValidationError(ValueError):
    """Raised when a transformed dataset fails validation."""


def validate_dataframe(df: pd.DataFrame, dataset_name: str) -> None:
    """Validate minimum quality requirements shared by all datasets."""

    if df.empty:
        raise DataValidationError(f"{dataset_name} is empty after transformation.")

    required_columns = {"source_dataset", "source_file"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise DataValidationError(f"{dataset_name} is missing required columns: {sorted(missing)}")

    if df.columns.duplicated().any():
        duplicated = df.columns[df.columns.duplicated()].tolist()
        raise DataValidationError(f"{dataset_name} has duplicated columns: {duplicated}")
