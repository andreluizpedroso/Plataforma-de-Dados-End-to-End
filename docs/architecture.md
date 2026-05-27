# Arquitetura

Este projeto usa uma arquitetura local que simula uma plataforma moderna de dados.

## Sistemas

### PostgreSQL OLTP

Representa o banco transacional da aplicacao. O foco aqui e integridade, constraints, indices e escrita concorrente.

### Python ingestion

Extrai dados da origem e grava arquivos Parquet na camada bronze. A ingestao deve ser idempotente: rodar duas vezes nao deve duplicar ou corromper dados.

### Parquet

Formato columnar eficiente para analise. Ele reduz leitura desnecessaria de colunas e funciona bem com DuckDB, Spark, Trino e engines cloud.

### DuckDB

Warehouse analitico local. Diferente do PostgreSQL, ele e orientado a OLAP e funciona muito bem para consultas agregadas em arquivos columnar.

### dbt

Camada de transformacao SQL, testes, documentacao e lineage. dbt ajuda a transformar regras de negocio em modelos versionados.

### Airflow

Orquestrador. Controla ordem, retries, agenda, logs e dependencias entre tarefas.

### Metabase

Camada de BI. Consome modelos gold para dashboards e exploracao de negocio.

## Camadas Medallion

### Bronze

Dado bruto, auditavel, com minimo de transformacao.

### Silver

Dado limpo, padronizado, tipado e deduplicado.

### Gold

Dado modelado para consumo analitico: fatos, dimensoes e metricas.
