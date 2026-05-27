from __future__ import annotations

import logging

import duckdb
import psycopg2
from psycopg2.extras import execute_values

from ingestion.src.config import Settings

LOGGER = logging.getLogger(__name__)


def publish_gold_to_postgres(settings: Settings) -> None:
    dataframe = _read_gold_positions(settings)

    with psycopg2.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE SCHEMA IF NOT EXISTS analytics")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS analytics.mart_account_positions (
                    account_id BIGINT NOT NULL,
                    account_number TEXT NOT NULL,
                    customer_id BIGINT NOT NULL,
                    full_name TEXT NOT NULL,
                    risk_profile TEXT NOT NULL,
                    asset_id BIGINT NOT NULL,
                    ticker TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    current_quantity NUMERIC(20, 8) NOT NULL,
                    invested_amount NUMERIC(20, 8) NOT NULL,
                    PRIMARY KEY (account_id, asset_id)
                )
                """
            )
            cursor.execute("TRUNCATE TABLE analytics.mart_account_positions")
            execute_values(
                cursor,
                """
                INSERT INTO analytics.mart_account_positions (
                    account_id,
                    account_number,
                    customer_id,
                    full_name,
                    risk_profile,
                    asset_id,
                    ticker,
                    asset_type,
                    current_quantity,
                    invested_amount
                )
                VALUES %s
                """,
                [tuple(row) for row in dataframe.itertuples(index=False, name=None)],
            )

    LOGGER.info("gold_published table=analytics.mart_account_positions rows=%s", len(dataframe))


def _read_gold_positions(settings: Settings):
    with duckdb.connect(str(settings.warehouse_path)) as connection:
        return connection.execute(
            """
            SELECT
                account_id,
                account_number,
                customer_id,
                full_name,
                risk_profile,
                asset_id,
                ticker,
                asset_type,
                current_quantity,
                invested_amount
            FROM main_gold.mart_account_positions
            ORDER BY account_number, ticker
            """
        ).fetchdf()
