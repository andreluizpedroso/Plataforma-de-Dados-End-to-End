INSERT INTO app.customers (full_name, email, document_number, birth_date, risk_profile)
VALUES
    ('Ana Ribeiro', 'ana.ribeiro@example.com', '11122233344', DATE '1988-04-12', 'moderate'),
    ('Bruno Martins', 'bruno.martins@example.com', '22233344455', DATE '1982-09-27', 'aggressive'),
    ('Carla Souza', 'carla.souza@example.com', '33344455566', DATE '1995-01-08', 'conservative')
ON CONFLICT (email) DO NOTHING;

INSERT INTO app.accounts (customer_id, account_number, account_status, opened_at)
SELECT customer_id, 'INV-0001', 'active', TIMESTAMPTZ '2025-01-03 10:00:00-03'
FROM app.customers
WHERE email = 'ana.ribeiro@example.com'
ON CONFLICT (account_number) DO NOTHING;

INSERT INTO app.accounts (customer_id, account_number, account_status, opened_at)
SELECT customer_id, 'INV-0002', 'active', TIMESTAMPTZ '2025-01-06 11:30:00-03'
FROM app.customers
WHERE email = 'bruno.martins@example.com'
ON CONFLICT (account_number) DO NOTHING;

INSERT INTO app.accounts (customer_id, account_number, account_status, opened_at)
SELECT customer_id, 'INV-0003', 'active', TIMESTAMPTZ '2025-01-10 09:15:00-03'
FROM app.customers
WHERE email = 'carla.souza@example.com'
ON CONFLICT (account_number) DO NOTHING;

INSERT INTO app.assets (ticker, asset_name, asset_type, exchange, currency_code)
VALUES
    ('PETR4', 'Petrobras PN', 'stock', 'B3', 'BRL'),
    ('ITUB4', 'Itau Unibanco PN', 'stock', 'B3', 'BRL'),
    ('MXRF11', 'Maxi Renda FII', 'fii', 'B3', 'BRL'),
    ('BOVA11', 'iShares Ibovespa Fundo de Indice', 'etf', 'B3', 'BRL'),
    ('TESOURO-SELIC-2029', 'Tesouro Selic 2029', 'fixed_income', 'Tesouro Direto', 'BRL')
ON CONFLICT (ticker) DO NOTHING;

INSERT INTO app.cash_transactions (account_id, transaction_type, amount, transaction_at, external_reference)
SELECT account_id, 'deposit', 25000.00, TIMESTAMPTZ '2025-01-15 09:00:00-03', 'seed-cash-0001'
FROM app.accounts
WHERE account_number = 'INV-0001'
ON CONFLICT (external_reference) DO NOTHING;

INSERT INTO app.cash_transactions (account_id, transaction_type, amount, transaction_at, external_reference)
SELECT account_id, 'deposit', 40000.00, TIMESTAMPTZ '2025-01-15 09:05:00-03', 'seed-cash-0002'
FROM app.accounts
WHERE account_number = 'INV-0002'
ON CONFLICT (external_reference) DO NOTHING;

INSERT INTO app.cash_transactions (account_id, transaction_type, amount, transaction_at, external_reference)
SELECT account_id, 'deposit', 12000.00, TIMESTAMPTZ '2025-01-15 09:10:00-03', 'seed-cash-0003'
FROM app.accounts
WHERE account_number = 'INV-0003'
ON CONFLICT (external_reference) DO NOTHING;

INSERT INTO app.orders (
    account_id,
    asset_id,
    order_side,
    order_type,
    order_status,
    quantity,
    limit_price,
    submitted_at
)
SELECT a.account_id, s.asset_id, 'buy', 'limit', 'filled', 100, 32.50, TIMESTAMPTZ '2025-01-16 10:01:00-03'
FROM app.accounts a
CROSS JOIN app.assets s
WHERE a.account_number = 'INV-0001'
  AND s.ticker = 'PETR4'
  AND NOT EXISTS (
      SELECT 1
      FROM app.orders existing
      WHERE existing.account_id = a.account_id
        AND existing.asset_id = s.asset_id
        AND existing.submitted_at = TIMESTAMPTZ '2025-01-16 10:01:00-03'
  );

INSERT INTO app.orders (
    account_id,
    asset_id,
    order_side,
    order_type,
    order_status,
    quantity,
    limit_price,
    submitted_at
)
SELECT a.account_id, s.asset_id, 'buy', 'limit', 'filled', 50, 105.20, TIMESTAMPTZ '2025-01-17 11:15:00-03'
FROM app.accounts a
CROSS JOIN app.assets s
WHERE a.account_number = 'INV-0002'
  AND s.ticker = 'BOVA11'
  AND NOT EXISTS (
      SELECT 1
      FROM app.orders existing
      WHERE existing.account_id = a.account_id
        AND existing.asset_id = s.asset_id
        AND existing.submitted_at = TIMESTAMPTZ '2025-01-17 11:15:00-03'
  );

INSERT INTO app.orders (
    account_id,
    asset_id,
    order_side,
    order_type,
    order_status,
    quantity,
    limit_price,
    submitted_at
)
SELECT a.account_id, s.asset_id, 'buy', 'limit', 'filled', 200, 10.15, TIMESTAMPTZ '2025-01-18 14:30:00-03'
FROM app.accounts a
CROSS JOIN app.assets s
WHERE a.account_number = 'INV-0003'
  AND s.ticker = 'MXRF11'
  AND NOT EXISTS (
      SELECT 1
      FROM app.orders existing
      WHERE existing.account_id = a.account_id
        AND existing.asset_id = s.asset_id
        AND existing.submitted_at = TIMESTAMPTZ '2025-01-18 14:30:00-03'
  );

INSERT INTO app.trades (order_id, executed_quantity, executed_price, brokerage_fee, executed_at)
SELECT order_id, quantity, limit_price, 0.00, submitted_at + INTERVAL '2 minutes'
FROM app.orders
WHERE order_status = 'filled'
  AND NOT EXISTS (
      SELECT 1
      FROM app.trades existing
      WHERE existing.order_id = app.orders.order_id
  );
