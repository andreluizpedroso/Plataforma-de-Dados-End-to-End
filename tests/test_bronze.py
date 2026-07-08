import pandas as pd

from ingestion.src import bronze as bronze_module
from ingestion.src.tables import SOURCE_TABLES
from conftest import make_settings


class _FakeConnection:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_extract_bronze_writes_one_parquet_per_source_table(tmp_path, monkeypatch):
    settings = make_settings(tmp_path)

    monkeypatch.setattr(bronze_module.psycopg2, "connect", lambda **kwargs: _FakeConnection())
    monkeypatch.setattr(
        bronze_module.pd,
        "read_sql_query",
        lambda query, connection: pd.DataFrame({"id": [1, 2]}),
    )

    bronze_module.extract_bronze(settings)

    for table_name in SOURCE_TABLES:
        output_path = settings.bronze_dir / f"{table_name}.parquet"
        assert output_path.exists()
        written = pd.read_parquet(output_path)
        assert "_extracted_at" in written.columns
        assert len(written) == 2


def test_bronze_path_builds_expected_filename(tmp_path):
    path = bronze_module._bronze_path(tmp_path, "customers")
    assert path == tmp_path / "customers.parquet"
