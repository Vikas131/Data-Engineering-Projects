# Weather Data ETL Pipeline

This project implements a fully containerized data pipeline that automates the flow of weather data from extraction to visualization.  
- **Extract**: Weather data is collected from the [Weatherstack API](https://weatherstack.com/).  
- **Load**: Raw JSON data are stored in **Postgres** database.  
- **Transform**: Data models are built with **dbt** to create clean, structured tables and analytical summaries.  
- **Orchestrate**: **Apache Airflow** schedules and manages each pipeline step.  
- **Visualize**: A curated data mart is connected to **Apache Superset** for interactive dashboards and analysis.  

All components run inside **Docker containers**, providing a reproducible and portable environment.

