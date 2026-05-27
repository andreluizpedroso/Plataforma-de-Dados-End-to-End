# Modern Data Engineering Platform

Projeto educacional para construir uma plataforma local de engenharia de dados ponta a ponta.

## Objetivo

Construir, entender e evoluir um pipeline com:

- PostgreSQL como banco transacional OLTP
- Python para ingestao e automacao
- Parquet como armazenamento intermediario columnar
- DuckDB como warehouse analitico local
- dbt para transformacoes SQL
- Airflow para orquestracao
- Metabase para BI
- Arquitetura Medallion: bronze, silver e gold

## Arquitetura inicial

```text
PostgreSQL OLTP
      |
      | Python ingestion
      v
data/bronze/*.parquet
      |
      | limpeza, tipagem, deduplicacao
      v
data/silver/*.parquet
      |
      | dbt + DuckDB
      v
warehouse/local.duckdb
      |
      | marts gold
      v
Metabase
```

## Estrutura

```text
.
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── plugins/
├── dashboards/
├── data/
│   ├── bronze/
│   ├── gold/
│   └── silver/
├── dbt/
├── docker/
│   └── postgres/
│       └── init/
├── docs/
├── ingestion/
│   └── src/
├── logs/
├── scripts/
├── tests/
├── warehouse/
├── .env.example
├── .gitignore
└── docker-compose.yml
```

## Como iniciar a infraestrutura

Copie `.env.example` para `.env` e ajuste se quiser.

```powershell
docker compose up -d postgres_oltp metabase airflow-init airflow-webserver airflow-scheduler
```

Servicos principais:

- PostgreSQL OLTP: `localhost:5432`
- Metabase: `http://localhost:3000`
- Airflow: `http://localhost:8080`

## Ordem de aprendizado

1. Modelagem OLTP no PostgreSQL.
2. Ingestao batch com Python.
3. Escrita idempotente em Parquet bronze.
4. Limpeza e incrementalidade em silver.
5. Modelagem dimensional gold com dbt.
6. Orquestracao com Airflow.
7. BI com Metabase.
8. Testes, observabilidade e CI/CD.

## Dominio inicial

O primeiro dominio do projeto e uma plataforma de investimentos.

Modelo OLTP inicial:

- `app.customers`
- `app.accounts`
- `app.assets`
- `app.orders`
- `app.trades`
- `app.cash_transactions`

Documentacao: `docs/oltp_investments_model.md`.

## Pipeline batch local

Depois que o PostgreSQL estiver no ar e populado pelos scripts de init:

```powershell
python -m pip install -r requirements.txt
python -m ingestion.src.pipeline --step all
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
```

O Airflow possui a DAG `investments_batch_pipeline`, que executa:

1. ingestao PostgreSQL -> Bronze/Silver/DuckDB
2. `dbt run`
3. `dbt test`
4. publica `main_gold.mart_account_positions` em `analytics.mart_account_positions` no PostgreSQL para o Metabase

Runbook operacional: `docs/runbook.md`.
