# Modelo OLTP de Investimentos

Este documento descreve o primeiro modelo transacional do projeto.

## Objetivo

Simular a origem de dados de uma plataforma de investimentos.

## Entidades

### customers

Representa o investidor.

Principais regras:

- email unico
- documento unico
- perfil de risco controlado por constraint

### accounts

Representa uma conta de investimento.

Uma conta pertence a um cliente. A relacao e 1:N porque um cliente pode ter mais de uma conta.

### assets

Representa o cadastro de ativos negociaveis.

Exemplos:

- acoes
- FIIs
- ETFs
- renda fixa
- caixa

### orders

Representa a intencao de compra ou venda enviada pelo cliente.

Uma ordem pode ser executada totalmente, parcialmente, cancelada ou rejeitada.

### trades

Representa a execucao real de uma ordem.

Uma ordem pode gerar varias execucoes parciais.

### cash_transactions

Representa movimentacoes de caixa, como deposito, retirada, dividendos, juros, taxas e impostos.

## Por que normalizar no OLTP?

Normalizacao reduz duplicidade e protege integridade. Em sistemas transacionais, isso e mais importante do que facilitar dashboards.

No futuro, a camada gold podera transformar esse modelo em dimensoes e fatos:

- dim_customers
- dim_accounts
- dim_assets
- fact_orders
- fact_trades
- fact_cash_transactions

## Decisoes importantes

### NUMERIC para valores financeiros

Valores financeiros nao devem usar FLOAT, porque FLOAT usa representacao aproximada.

### Constraints CHECK

As constraints evitam estados invalidos perto da origem.

### Timestamps com timezone

Eventos financeiros dependem de tempo. `TIMESTAMPTZ` evita ambiguidades em ambientes com fusos diferentes.

### Indices

Os indices iniciais suportam buscas por cliente, conta, ativo e tempo, que sao padroes comuns em sistemas financeiros.
