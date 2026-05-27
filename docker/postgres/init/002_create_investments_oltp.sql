CREATE TABLE IF NOT EXISTS app.customers (
    customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    document_number TEXT NOT NULL UNIQUE,
    birth_date DATE NOT NULL,
    risk_profile TEXT NOT NULL CHECK (risk_profile IN ('conservative', 'moderate', 'aggressive')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS app.accounts (
    account_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES app.customers (customer_id),
    account_number TEXT NOT NULL UNIQUE,
    account_status TEXT NOT NULL CHECK (account_status IN ('active', 'blocked', 'closed')),
    opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (closed_at IS NULL OR closed_at >= opened_at)
);

CREATE TABLE IF NOT EXISTS app.assets (
    asset_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticker TEXT NOT NULL UNIQUE,
    asset_name TEXT NOT NULL,
    asset_type TEXT NOT NULL CHECK (asset_type IN ('stock', 'fii', 'etf', 'fixed_income', 'cash')),
    exchange TEXT NOT NULL,
    currency_code CHAR(3) NOT NULL DEFAULT 'BRL',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS app.orders (
    order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id BIGINT NOT NULL REFERENCES app.accounts (account_id),
    asset_id BIGINT NOT NULL REFERENCES app.assets (asset_id),
    order_side TEXT NOT NULL CHECK (order_side IN ('buy', 'sell')),
    order_type TEXT NOT NULL CHECK (order_type IN ('market', 'limit')),
    order_status TEXT NOT NULL CHECK (order_status IN ('new', 'partially_filled', 'filled', 'cancelled', 'rejected')),
    quantity NUMERIC(20, 8) NOT NULL CHECK (quantity > 0),
    limit_price NUMERIC(20, 8),
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (
        (order_type = 'market' AND limit_price IS NULL)
        OR
        (order_type = 'limit' AND limit_price IS NOT NULL AND limit_price > 0)
    )
);

CREATE TABLE IF NOT EXISTS app.trades (
    trade_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES app.orders (order_id),
    executed_quantity NUMERIC(20, 8) NOT NULL CHECK (executed_quantity > 0),
    executed_price NUMERIC(20, 8) NOT NULL CHECK (executed_price > 0),
    brokerage_fee NUMERIC(20, 8) NOT NULL DEFAULT 0 CHECK (brokerage_fee >= 0),
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS app.cash_transactions (
    cash_transaction_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id BIGINT NOT NULL REFERENCES app.accounts (account_id),
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('deposit', 'withdrawal', 'dividend', 'interest', 'fee', 'tax')),
    amount NUMERIC(20, 8) NOT NULL CHECK (amount > 0),
    currency_code CHAR(3) NOT NULL DEFAULT 'BRL',
    transaction_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    external_reference TEXT UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_accounts_customer_id
    ON app.accounts (customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_account_submitted_at
    ON app.orders (account_id, submitted_at);

CREATE INDEX IF NOT EXISTS idx_orders_asset_id
    ON app.orders (asset_id);

CREATE INDEX IF NOT EXISTS idx_trades_order_id
    ON app.trades (order_id);

CREATE INDEX IF NOT EXISTS idx_trades_executed_at
    ON app.trades (executed_at);

CREATE INDEX IF NOT EXISTS idx_cash_transactions_account_transaction_at
    ON app.cash_transactions (account_id, transaction_at);

COMMENT ON TABLE app.customers IS 'Investidores cadastrados na plataforma transacional.';
COMMENT ON TABLE app.accounts IS 'Contas de investimento pertencentes aos clientes.';
COMMENT ON TABLE app.assets IS 'Catalogo transacional de ativos negociaveis.';
COMMENT ON TABLE app.orders IS 'Ordens enviadas por contas de investimento.';
COMMENT ON TABLE app.trades IS 'Execucoes financeiras geradas a partir de ordens.';
COMMENT ON TABLE app.cash_transactions IS 'Movimentacoes financeiras de caixa das contas.';
