import pandas as pd

from ingestion.src.silver import _deduplicate, _standardize_columns


def test_standardize_columns_lowercases_and_strips_names():
    dataframe = pd.DataFrame({" Customer_ID ": [1], "Email": ["a@example.com"]})

    standardized = _standardize_columns(dataframe)

    assert list(standardized.columns) == ["customer_id", "email"]


def test_deduplicate_keeps_latest_record_by_updated_at():
    dataframe = pd.DataFrame(
        {
            "customer_id": [1, 1],
            "email": ["old@example.com", "new@example.com"],
            "updated_at": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        }
    )

    deduplicated = _deduplicate(dataframe, "customers")

    assert len(deduplicated) == 1
    assert deduplicated.iloc[0]["email"] == "new@example.com"
