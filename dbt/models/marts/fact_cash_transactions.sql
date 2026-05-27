SELECT
    cash_transaction_id,
    account_id,
    transaction_type,
    amount,
    CASE
        WHEN transaction_type IN ('deposit', 'dividend', 'interest') THEN amount
        WHEN transaction_type IN ('withdrawal', 'fee', 'tax') THEN -amount
    END AS signed_amount,
    currency_code,
    transaction_at,
    external_reference
FROM {{ ref('stg_cash_transactions') }}
