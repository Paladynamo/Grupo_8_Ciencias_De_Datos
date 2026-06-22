from pathlib import Path

import pandas as pd

from etl.transform.common import clean_dataframe, normalize_column_name, parse_currency_series, parse_percent_series


def test_normalize_column_name_uses_snake_case() -> None:
    assert normalize_column_name("Attack Points (%)") == "attack_points"


def test_clean_dataframe_adds_source_metadata_and_drops_duplicates() -> None:
    df = pd.DataFrame({" Card Name ": ["A", "A"], "Value": [1, 1]})

    cleaned = clean_dataframe(df, source_name="sample", source_file=Path("cards.csv"))

    assert len(cleaned) == 1
    assert "card_name" in cleaned.columns
    assert cleaned.loc[0, "source_dataset"] == "sample"
    assert cleaned.loc[0, "source_file"] == "cards.csv"


def test_parse_percent_series_returns_numeric_values() -> None:
    result = parse_percent_series(pd.Series(["54.189%", "bad"]))

    assert result.iloc[0] == 54.189
    assert pd.isna(result.iloc[1])


def test_parse_currency_series_returns_numeric_values() -> None:
    result = parse_currency_series(pd.Series(["$37.32", "bad"]))

    assert result.iloc[0] == 37.32
    assert pd.isna(result.iloc[1])
