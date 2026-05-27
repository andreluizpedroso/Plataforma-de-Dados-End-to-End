from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="investments_batch_pipeline",
    description="Batch pipeline from PostgreSQL OLTP to DuckDB gold marts.",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["investments", "medallion", "duckdb", "dbt"],
) as dag:
    ingest_to_duckdb = BashOperator(
        task_id="ingest_to_duckdb",
        bash_command=(
            "cd /opt/airflow && "
            "PROJECT_ROOT=/opt/airflow "
            "python -m ingestion.src.pipeline --step all"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow && dbt run --project-dir dbt --profiles-dir dbt",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow && dbt test --project-dir dbt --profiles-dir dbt",
    )

    publish_gold = BashOperator(
        task_id="publish_gold",
        bash_command=(
            "cd /opt/airflow && "
            "PROJECT_ROOT=/opt/airflow "
            "python -m ingestion.src.pipeline --step publish"
        ),
    )

    ingest_to_duckdb >> dbt_run >> dbt_test >> publish_gold
