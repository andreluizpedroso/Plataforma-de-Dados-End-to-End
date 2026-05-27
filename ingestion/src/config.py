from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    project_root: Path
    bronze_dir: Path
    silver_dir: Path
    warehouse_path: Path

    @property
    def sqlalchemy_url(self) -> str:
        return (
            "postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def load_settings() -> Settings:
    project_root = Path(os.getenv("PROJECT_ROOT", ".")).resolve()

    return Settings(
        postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
        postgres_port=int(os.getenv("POSTGRES_PORT", "5432")),
        postgres_db=os.getenv("POSTGRES_DB", "app_db"),
        postgres_user=os.getenv("POSTGRES_USER", "app_user"),
        postgres_password=os.getenv("POSTGRES_PASSWORD", "app_password"),
        project_root=project_root,
        bronze_dir=project_root / "data" / "bronze",
        silver_dir=project_root / "data" / "silver",
        warehouse_path=project_root / "warehouse" / "investments.duckdb",
    )
