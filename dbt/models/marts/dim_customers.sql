SELECT
    customer_id,
    full_name,
    email,
    risk_profile,
    birth_date,
    created_at
FROM {{ ref('stg_customers') }}
