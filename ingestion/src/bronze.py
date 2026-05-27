from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import psycopg2

from ingestion.src.config import Settings
from ingestion.src.tables import SOURCE_TABLES

LOGGER = logging.getLogger(__name__)


def extract_bronze(settings: Settings) -> None:
    settings.bronze_dir.mkdir(parents=True, exist_ok=True)
    extracted_at = datetime.now(timezone.utc).isoformat()

    with psycopg2.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
    ) as connection:
        for table_name in SOURCE_TABLES:
            query = f"SELECT * FROM app.{table_name}"
            dataframe = pd.read_sql_query(query, connection)
            dataframe["_extracted_at"] = extracted_at
            output_path = _bronze_path(settings.bronze_dir, table_name)
            dataframe.to_parquet(output_path, index=False)
            LOGGER.info("bronze_written table=%s rows=%s path=%s", table_name, len(dataframe), output_path)


def _bronze_path(bronze_dir: Path, table_name: str) -> Path:
    return bronze_dir / f"{table_name}.parquet"
