SELECT
    cash_transaction_id,
    account_id,
    transaction_type,
    amount,
    currency_code,
    transaction_at,
    external_reference,
    created_at
FROM {{ source('silver', 'cash_transactions') }}
