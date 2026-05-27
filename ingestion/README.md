# Ingestion

Camada de codigo Python responsavel por extrair dados das origens e gravar a camada bronze.

Principios:

- idempotencia
- logs estruturados
- tratamento de erro
- retries quando fizer sentido
- separacao entre configuracao, extracao e escrita
