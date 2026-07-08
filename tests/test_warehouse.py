import duckdb
import pandas as pd

from ingestion.src.tables import SOURCE_TABLES
from ingestion.src.warehouse import load_duckdb
from conftest import make_settings


def test_load_duckdb_creates_silver_tables_from_parquet(tmp_path):
    settings = make_settings(tmp_path)
    settings.silver_dir.mkdir(parents=True)

    for table_name in SOURCE_TABLES:
        dataframe = pd.DataFrame({"id": [1, 2], "value": ["a", "b"]})
        dataframe.to_parquet(settings.silver_dir / f"{table_name}.parquet", index=False)

    load_duckdb(settings)

    assert settings.warehouse_path.exists()
    with duckdb.connect(str(settings.warehouse_path)) as connection:
        for table_name in SOURCE_TABLES:
            count = connection.execute(f"SELECT COUNT(*) FROM silver.{table_name}").fetchone()[0]
            assert count == 2
