SELECT
    asset_id,
    ticker,
    asset_name,
    asset_type,
    exchange,
    currency_code,
    is_active,
    created_at,
    updated_at
FROM {{ source('silver', 'assets') }}
