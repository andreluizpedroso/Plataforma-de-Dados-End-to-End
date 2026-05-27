SELECT
    asset_id,
    ticker,
    asset_name,
    asset_type,
    exchange,
    currency_code,
    is_active
FROM {{ ref('stg_assets') }}
