import duckdb

from ingestion.src import publish as publish_module
from conftest import make_settings


def _seed_gold_warehouse(warehouse_path):
    warehouse_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(warehouse_path)) as connection:
        connection.execute("CREATE SCHEMA main_gold")
        connection.execute(
            """
            CREATE TABLE main_gold.mart_account_positions (
                account_id BIGINT,
                account_number TEXT,
                customer_id BIGINT,
                full_name TEXT,
                risk_profile TEXT,
                asset_id BIGINT,
                ticker TEXT,
                asset_type TEXT,
                current_quantity DOUBLE,
                invested_amount DOUBLE
            )
            """
        )
        connection.execute(
            """
            INSERT INTO main_gold.mart_account_positions VALUES
            (1, 'AC-1', 10, 'Ana', 'moderado', 100, 'PETR4', 'acao', 50.0, 1000.0)
            """
        )


def test_read_gold_positions_returns_expected_data(tmp_path):
    settings = make_settings(tmp_path)
    _seed_gold_warehouse(settings.warehouse_path)

    dataframe = publish_module._read_gold_positions(settings)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["ticker"] == "PETR4"
    assert dataframe.iloc[0]["account_number"] == "AC-1"


class _FakeCursor:
    def __init__(self, executed):
        self._executed = executed

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql, *args):
        self._executed.append(sql.strip().split()[0].upper())


class _FakeConnection:
    def __init__(self, executed):
        self._executed = executed

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def cursor(self):
        return _FakeCursor(self._executed)


def test_publish_gold_to_postgres_creates_schema_table_and_inserts(tmp_path, monkeypatch):
    settings = make_settings(tmp_path)
    _seed_gold_warehouse(settings.warehouse_path)

    executed = []
    monkeypatch.setattr(publish_module.psycopg2, "connect", lambda **kwargs: _FakeConnection(executed))
    monkeypatch.setattr(publish_module, "execute_values", lambda cursor, sql, rows: executed.append("INSERT"))

    publish_module.publish_gold_to_postgres(settings)

    assert "CREATE" in executed
    assert "TRUNCATE" in executed
    assert "INSERT" in executed
