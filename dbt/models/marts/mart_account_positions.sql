WITH trade_positions AS (
    SELECT
        account_id,
        asset_id,
        SUM(signed_quantity) AS current_quantity,
        SUM(gross_amount + brokerage_fee) AS invested_amount
    FROM {{ ref('fact_trades') }}
    GROUP BY 1, 2
),

accounts AS (
    SELECT *
    FROM {{ ref('dim_accounts') }}
),

customers AS (
    SELECT *
    FROM {{ ref('dim_customers') }}
),

assets AS (
    SELECT *
    FROM {{ ref('dim_assets') }}
)

SELECT
    accounts.account_id,
    accounts.account_number,
    customers.customer_id,
    customers.full_name,
    customers.risk_profile,
    assets.asset_id,
    assets.ticker,
    assets.asset_type,
    trade_positions.current_quantity,
    trade_positions.invested_amount
FROM trade_positions
INNER JOIN accounts
    ON trade_positions.account_id = accounts.account_id
INNER JOIN customers
    ON accounts.customer_id = customers.customer_id
INNER JOIN assets
    ON trade_positions.asset_id = assets.asset_id
