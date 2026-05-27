SELECT
    trade_id,
    order_id,
    executed_quantity,
    executed_price,
    brokerage_fee,
    executed_at,
    created_at
FROM {{ source('silver', 'trades') }}
