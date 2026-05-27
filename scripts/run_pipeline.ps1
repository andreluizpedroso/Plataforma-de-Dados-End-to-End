$ErrorActionPreference = "Stop"

python -m ingestion.src.pipeline --step all
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
python -m ingestion.src.pipeline --step publish
