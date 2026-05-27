from ingestion.src.config import load_settings


def test_load_settings_uses_project_root(monkeypatch, tmp_path):
    monkeypatch.setenv("PROJECT_ROOT", str(tmp_path))

    settings = load_settings()

    assert settings.bronze_dir == tmp_path / "data" / "bronze"
    assert settings.silver_dir == tmp_path / "data" / "silver"
    assert settings.warehouse_path == tmp_path / "warehouse" / "investments.duckdb"
