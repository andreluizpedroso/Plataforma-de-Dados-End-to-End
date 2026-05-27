# Runbook Operacional

Este runbook descreve como operar o projeto localmente.

## Subir infraestrutura

```powershell
docker compose up -d postgres_oltp metabase airflow-init airflow-webserver airflow-scheduler
```

Se o Docker falhar com erro de pipe no Windows, abra o Docker Desktop e tente novamente.

## Rodar pipeline local

```powershell
python -m ingestion.src.pipeline --step all
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
python -m ingestion.src.pipeline --step publish
```

Se `dbt` nao estiver no PATH:

```powershell
python -m dbt.cli.main run --project-dir dbt --profiles-dir dbt
python -m dbt.cli.main test --project-dir dbt --profiles-dir dbt
```

## Validar camada Gold sem PostgreSQL

```powershell
python scripts/create_demo_duckdb.py
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
```

## Testes Python

```powershell
python -m pytest tests
```

## Debug

Verificar configuracao dbt:

```powershell
dbt debug --project-dir dbt --profiles-dir dbt
```

Verificar parse dos modelos:

```powershell
dbt parse --project-dir dbt --profiles-dir dbt
```

Verificar Compose:

```powershell
docker compose config
```

## Monitoramento local

- Airflow UI: `http://localhost:8080`
- Metabase: `http://localhost:3000`
- Logs do Airflow: `airflow/logs`
- Logs de execucao Python: stdout da task ou terminal

## Falhas comuns

- Docker Desktop fechado.
- Volume antigo do PostgreSQL impedindo scripts de init novos.
- `dbt run` e `dbt test` rodando ao mesmo tempo em DuckDB.
- Dependencias instaladas em um Python diferente do Python usado para executar.
- Caminhos relativos diferentes entre execucao local e execucao em container.
