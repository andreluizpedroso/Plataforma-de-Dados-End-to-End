from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from ingestion.src.config import Settings
from ingestion.src.tables import SOURCE_TABLES

LOGGER = logging.getLogger(__name__)

PRIMARY_KEYS = {
    "customers": ["customer_id"],
    "accounts": ["account_id"],
    "assets": ["asset_id"],
    "orders": ["order_id"],
    "trades": ["trade_id"],
    "cash_transactions": ["cash_transaction_id"],
}


def build_silver(settings: Settings) -> None:
    settings.silver_dir.mkdir(parents=True, exist_ok=True)

    for table_name in SOURCE_TABLES:
        bronze_path = settings.bronze_dir / f"{table_name}.parquet"
        silver_path = settings.silver_dir / f"{table_name}.parquet"

        dataframe = pd.read_parquet(bronze_path)
        dataframe = _standardize_columns(dataframe)
        dataframe = _deduplicate(dataframe, table_name)
        dataframe.to_parquet(silver_path, index=False)
        LOGGER.info("silver_written table=%s rows=%s path=%s", table_name, len(dataframe), silver_path)


def _standardize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    standardized = dataframe.copy()
    standardized.columns = [column.strip().lower() for column in standardized.columns]
    return standardized


def _deduplicate(dataframe: pd.DataFrame, table_name: str) -> pd.DataFrame:
    primary_key = PRIMARY_KEYS[table_name]
    sort_columns = [column for column in ["updated_at", "created_at", "_extracted_at"] if column in dataframe.columns]

    if sort_columns:
        dataframe = dataframe.sort_values(sort_columns)

    return dataframe.drop_duplicates(subset=primary_key, keep="last")
