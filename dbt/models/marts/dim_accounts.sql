SELECT
    account_id,
    customer_id,
    account_number,
    account_status,
    opened_at,
    closed_at
FROM {{ ref('stg_accounts') }}
