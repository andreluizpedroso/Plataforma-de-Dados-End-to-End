SELECT
    order_id,
    account_id,
    asset_id,
    order_side,
    order_type,
    order_status,
    quantity,
    limit_price,
    submitted_at,
    updated_at
FROM {{ source('silver', 'orders') }}
