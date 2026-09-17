# Agro-climatic Data Pipeline

Data pipeline that cross-references INMET daily weather series with IBGE municipal
agricultural production data to answer whether climate variation explains
productivity variation by crop and municipality.

## Architecture

```mermaid
flowchart LR
    INMET[INMET API<br/>daily weather] --> ING[Ingestion<br/>Python + requests]
    IBGE[IBGE SIDRA<br/>crop production] --> ING
    ING --> MONGO[(MongoDB<br/>raw JSON)]
    ING --> BRONZE[Azure Blob<br/>Parquet partitioned]
    BRONZE --> SILVER[PySpark<br/>cleaning + validation]
    SILVER --> QUAR[(Quarantine<br/>rejected records)]
    SILVER --> GOLD[(PostgreSQL<br/>dimensional model)]
    GOLD --> SQL[Analytical SQL]
```

Medallion architecture (bronze/silver/gold), orchestrated with Airflow and running
on Docker Compose.

## Stack

| Layer | Tool | Rationale |
|---|---|---|
| Ingestion | Python + requests | API consumption with pagination, retry and rate limiting |
| Raw | MongoDB | Semi-structured payload with unstable schema; storing it raw allows reprocessing without calling the API again |
| Bronze | Azure Blob + Parquet | Cheap storage, columnar format, partitioned by date |
| Silver | PySpark | Same API as a cluster, even running locally |
| Gold | PostgreSQL | Dimensional model for analytical queries |
| Orchestration | Airflow | Daily DAG, task dependencies, retry, backfill |
| Infrastructure | Docker Compose | Reproducible environment with a single command |

## Data sources

- **INMET** — daily weather data from automatic stations (temperature, rainfall, humidity)
- **IBGE / SIDRA** — Municipal Agricultural Production: planted area, output and average yield by municipality and crop

## Getting started

```bash
cp .env.example .env    # fill in your credentials
docker compose up -d
docker compose ps       # postgres and mongo should report healthy
```

## Project status

Work in progress. Current stage: bronze ingestion.

- [x] Local environment (PostgreSQL + MongoDB via Docker Compose)
- [ ] INMET ingestion with retry and structured logging
- [ ] Bronze layer as partitioned Parquet on Azure Blob
- [ ] Silver layer with data quality validation and quarantine
- [ ] Dimensional model in the gold layer
- [ ] Airflow orchestration
- [ ] Final analysis and documented results

## Roadmap

Sections to be added as the project evolves:

- **Technical decisions** — idempotency, partitioning strategy, incremental load
- **Data quality** — implemented rules and observed metrics
- **Results** — processed volume, runtime, rejection rate, analytical findings
- **Limitations and next steps**