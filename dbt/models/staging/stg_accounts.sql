SELECT
    account_id,
    customer_id,
    account_number,
    account_status,
    opened_at,
    closed_at,
    created_at,
    updated_at
FROM {{ source('silver', 'accounts') }}
