from __future__ import annotations

import logging

import duckdb

from ingestion.src.config import Settings
from ingestion.src.tables import SOURCE_TABLES

LOGGER = logging.getLogger(__name__)


def load_duckdb(settings: Settings) -> None:
    settings.warehouse_path.parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(settings.warehouse_path)) as connection:
        connection.execute("CREATE SCHEMA IF NOT EXISTS silver")

        for table_name in SOURCE_TABLES:
            parquet_path = (settings.silver_dir / f"{table_name}.parquet").as_posix()
            connection.execute(
                f"""
                CREATE OR REPLACE TABLE silver.{table_name} AS
                SELECT *
                FROM read_parquet(?)
                """,
                [parquet_path],
            )
            row_count = connection.execute(f"SELECT COUNT(*) FROM silver.{table_name}").fetchone()[0]
            LOGGER.info("duckdb_loaded table=silver.%s rows=%s", table_name, row_count)
