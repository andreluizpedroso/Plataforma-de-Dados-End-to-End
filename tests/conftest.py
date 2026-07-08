from ingestion.src.config import Settings


def make_settings(tmp_path) -> Settings:
    return Settings(
        postgres_host="localhost",
        postgres_port=5432,
        postgres_db="app_db",
        postgres_user="app_user",
        postgres_password="app_password",
        project_root=tmp_path,
        bronze_dir=tmp_path / "data" / "bronze",
        silver_dir=tmp_path / "data" / "silver",
        warehouse_path=tmp_path / "warehouse" / "investments.duckdb",
    )
