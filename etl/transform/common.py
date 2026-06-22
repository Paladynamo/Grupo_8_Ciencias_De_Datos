"""Shared transformation helpers."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


def normalize_column_name(column: object) -> str:
    """Convert a column name to lower snake_case."""

    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", str(column).strip().lower())
    return re.sub(r"_+", "_", normalized).strip("_")


def clean_dataframe(df: pd.DataFrame, source_name: str, source_file: Path) -> pd.DataFrame:
    """Apply safe, source-agnostic cleaning that does not depend on final analysis choices."""

    cleaned = df.copy()
    cleaned.columns = [normalize_column_name(col) for col in cleaned.columns]
    cleaned = cleaned.drop_duplicates()
    cleaned["source_dataset"] = source_name
    cleaned["source_file"] = source_file.name
    return cleaned


def parse_percent_series(series: pd.Series) -> pd.Series:
    """Convert strings like '54.189%' to numeric percentages."""

    return pd.to_numeric(series.astype(str).str.replace("%", "", regex=False), errors="coerce")


def parse_currency_series(series: pd.Series) -> pd.Series:
    """Convert currency strings like '$37.32' to numeric values."""

    return pd.to_numeric(series.astype(str).str.replace("$", "", regex=False), errors="coerce")


def read_tabular_file(path: Path) -> pd.DataFrame:
    """Read a CSV or Excel file using Pandas."""

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported tabular file: {path}")
