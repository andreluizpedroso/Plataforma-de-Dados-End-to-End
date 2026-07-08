import pandas as pd

from ingestion.src.silver import PRIMARY_KEYS, _deduplicate, _standardize_columns, build_silver
from conftest import make_settings


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


def test_build_silver_reads_bronze_and_writes_deduped_standardized_silver(tmp_path):
    settings = make_settings(tmp_path)
    settings.bronze_dir.mkdir(parents=True)

    for table_name, primary_key in PRIMARY_KEYS.items():
        pk_column = primary_key[0]
        dataframe = pd.DataFrame(
            {
                f" {pk_column} ": [1, 1],
                " Email ": ["old@example.com", "new@example.com"],
                "_extracted_at": ["2025-01-01", "2025-01-02"],
            }
        )
        dataframe.to_parquet(settings.bronze_dir / f"{table_name}.parquet", index=False)

    build_silver(settings)

    for table_name, primary_key in PRIMARY_KEYS.items():
        pk_column = primary_key[0]
        silver_path = settings.silver_dir / f"{table_name}.parquet"
        assert silver_path.exists()
        result = pd.read_parquet(silver_path)
        assert list(result.columns) == [pk_column, "email", "_extracted_at"]
        assert len(result) == 1
        assert result.iloc[0]["email"] == "new@example.com"
