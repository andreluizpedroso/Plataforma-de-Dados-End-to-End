from __future__ import annotations

from pathlib import Path

import duckdb


WAREHOUSE_PATH = Path("warehouse/investments.duckdb")


def main() -> None:
    WAREHOUSE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(WAREHOUSE_PATH)) as connection:
        connection.execute("CREATE SCHEMA IF NOT EXISTS silver")

        connection.execute(
            """
            CREATE OR REPLACE TABLE silver.customers AS
            SELECT
                1::BIGINT AS customer_id,
                'Ana Ribeiro' AS full_name,
                'ana.ribeiro@example.com' AS email,
                '11122233344' AS document_number,
                DATE '1988-04-12' AS birth_date,
                'moderate' AS risk_profile,
                TIMESTAMP '2025-01-03 10:00:00' AS created_at,
                TIMESTAMP '2025-01-03 10:00:00' AS updated_at
            """
        )

        connection.execute(
            """
            CREATE OR REPLACE TABLE silver.accounts AS
            SELECT
                1::BIGINT AS account_id,
                1::BIGINT AS customer_id,
                'INV-0001' AS account_number,
                'active' AS account_status,
                TIMESTAMP '2025-01-03 10:00:00' AS opened_at,
                NULL::TIMESTAMP AS closed_at,
                TIMESTAMP '2025-01-03 10:00:00' AS created_at,
                TIMESTAMP '2025-01-03 10:00:00' AS updated_at
            """
        )

        connection.execute(
            """
            CREATE OR REPLACE TABLE silver.assets AS
            SELECT
                1::BIGINT AS asset_id,
                'PETR4' AS ticker,
                'Petrobras PN' AS asset_name,
                'stock' AS asset_type,
                'B3' AS exchange,
                'BRL' AS currency_code,
                TRUE AS is_active,
                TIMESTAMP '2025-01-03 10:00:00' AS created_at,
                TIMESTAMP '2025-01-03 10:00:00' AS updated_at
            """
        )

        connection.execute(
            """
            CREATE OR REPLACE TABLE silver.orders AS
            SELECT
                1::BIGINT AS order_id,
                1::BIGINT AS account_id,
                1::BIGINT AS asset_id,
                'buy' AS order_side,
                'limit' AS order_type,
                'filled' AS order_status,
                100.0::DECIMAL(20, 8) AS quantity,
                32.5::DECIMAL(20, 8) AS limit_price,
                TIMESTAMP '2025-01-16 10:01:00' AS submitted_at,
                TIMESTAMP '2025-01-16 10:03:00' AS updated_at
            """
        )

        connection.execute(
            """
            CREATE OR REPLACE TABLE silver.trades AS
            SELECT
                1::BIGINT AS trade_id,
                1::BIGINT AS order_id,
                100.0::DECIMAL(20, 8) AS executed_quantity,
                32.5::DECIMAL(20, 8) AS executed_price,
                0.0::DECIMAL(20, 8) AS brokerage_fee,
                TIMESTAMP '2025-01-16 10:03:00' AS executed_at,
                TIMESTAMP '2025-01-16 10:03:00' AS created_at
            """
        )

        connection.execute(
            """
            CREATE OR REPLACE TABLE silver.cash_transactions AS
            SELECT
                1::BIGINT AS cash_transaction_id,
                1::BIGINT AS account_id,
                'deposit' AS transaction_type,
                25000.0::DECIMAL(20, 8) AS amount,
                'BRL' AS currency_code,
                TIMESTAMP '2025-01-15 09:00:00' AS transaction_at,
                'seed-cash-0001' AS external_reference,
                TIMESTAMP '2025-01-15 09:00:00' AS created_at
            """
        )


if __name__ == "__main__":
    main()
