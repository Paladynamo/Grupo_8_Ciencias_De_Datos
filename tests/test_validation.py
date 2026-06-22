import pandas as pd
import pytest

from etl.validation import DataValidationError, validate_dataframe


def test_validate_dataframe_rejects_empty_dataframes() -> None:
    df = pd.DataFrame(columns=["source_dataset", "source_file"])

    with pytest.raises(DataValidationError):
        validate_dataframe(df, dataset_name="empty")


def test_validate_dataframe_accepts_minimum_metadata() -> None:
    df = pd.DataFrame({"source_dataset": ["pokemon"], "source_file": ["file.csv"]})

    validate_dataframe(df, dataset_name="pokemon")
