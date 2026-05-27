$ErrorActionPreference = "Stop"

docker compose up -d postgres_oltp metabase airflow-init airflow-webserver airflow-scheduler
