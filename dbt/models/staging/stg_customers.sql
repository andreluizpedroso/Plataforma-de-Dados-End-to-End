SELECT
    customer_id,
    full_name,
    email,
    document_number,
    birth_date,
    risk_profile,
    created_at,
    updated_at
FROM {{ source('silver', 'customers') }}
