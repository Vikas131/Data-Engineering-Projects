# Weather Data ETL Pipeline

## Project Overview
This project implements a fully containerized data pipeline for automating the extraction, storage, transformation, and visualization of weather data.  
Weather data is extracted from the [Weatherstack API](https://weatherstack.com/) and ingested into a **Postgres** database as raw JSON. Using **dbt**, the raw data is cleaned, structured, and aggregated into analytics-ready models. The entire workflow is orchestrated with **Apache Airflow**, ensuring automated scheduling and monitoring. Finally, the curated datasets are visualized in **Apache Superset** dashboards for insights into daily and historical weather trends.  

The pipeline is designed for **reproducibility, scalability, and easy deployment**, all running seamlessly inside **Docker containers**.

## Features

- **Automated Orchestration**: Apache Airflow schedules and manages the pipeline.  
- **Containerized Deployment**: Docker ensures easy setup and reproducibility.  
- **Reliable Data Ingestion**: Weatherstack API data stored as raw JSON in Postgres.  
- **Structured Transformations**: dbt cleans and aggregates data into analytics-ready tables.  
- **Interactive Dashboards**: Superset visualizations for trend analysis and reporting.  
- **Scalable & Extensible**: Easily add new locations, parameters, or data sources.  
- **Reproducible & Reliable**: Idempotent ingestion and dbt tests ensure data quality.

## Architecture

The pipeline follows an **Extract → Load → Transform → Visualize** workflow:

![Architecture Diagram](./images/data_flow.png)


## Workflow Details

1. **Extract & Load**  
   - `extract.py` fetches weather data from the Weatherstack API.  
   - `insert_data.py` stores the raw JSON into Postgres (`raw_data` table).  

2. **Transform**  
   - dbt reads raw data from Postgres, cleans and structures it.  
   - Creates two analytics-ready tables:  
     - `daily_average` → aggregates daily weather metrics  
     - `weather_report` → curated dataset for reporting and dashboards  

3. **Visualize**  
   - Apache Superset connects to Postgres and builds interactive dashboards using the two data marts.  

4. **Orchestration**  
   - Apache Airflow schedules and monitors all steps automatically.

