WITH trades AS (
    SELECT *
    FROM {{ ref('stg_trades') }}
),

orders AS (
    SELECT *
    FROM {{ ref('stg_orders') }}
)

SELECT
    trades.trade_id,
    orders.order_id,
    orders.account_id,
    orders.asset_id,
    orders.order_side,
    trades.executed_quantity,
    trades.executed_price,
    trades.brokerage_fee,
    trades.executed_quantity * trades.executed_price AS gross_amount,
    CASE
        WHEN orders.order_side = 'buy' THEN trades.executed_quantity
        WHEN orders.order_side = 'sell' THEN -trades.executed_quantity
    END AS signed_quantity,
    trades.executed_at
FROM trades
INNER JOIN orders
    ON trades.order_id = orders.order_id
