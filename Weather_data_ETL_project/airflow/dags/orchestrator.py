import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import Mount


sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_data import main
    return main()

args = {
    'description': 'A DAG to orchestrate weather api data',
    'start_date': datetime(2025,8,13),
    'catchup' : False
}

dag = DAG(
    dag_id = 'weather_api_dbt_orchestrator',
    default_args = args,
    schedule = timedelta(minutes=5)
)

with dag:
    task1 = PythonOperator(
        task_id = 'extract_data_task',
        python_callable = safe_main_callable
    )

    task2 = DockerOperator(
        task_id = 'transform_data_task',
        image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command = 'run',
        working_dir = '/usr/app',
        mounts=[
          # replace XXXX withh your path
            Mount(source='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/dbt/my_project',
                  target='/usr/app',
                  type='bind'),
            Mount(source='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/dbt/profiles.yml',
                  target='/root/.dbt/profiles.yml',
                  type='bind')
        ],
        network_mode='weatherapi_etl_project_my-network',
        docker_url = 'unix://var/run/docker.sock',
        auto_remove = 'success'
    )

    task1 >> task2
