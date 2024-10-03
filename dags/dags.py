from dotenv import load_dotenv
import os
import sys

load_dotenv()
work_dir = os.getenv('WORK_DIR')
sys.path.append(work_dir)
print(os.getenv('PYTHONASYNCIODEBUG'))

sys.path.append('/home/manuel/Escritorio/proyecto_ETL/ETL-1')


from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from datetime import datetime
from dags.etl import *



# Definir los argumentos por defecto para las tareas
default_args = {
    'owner': 'Airflow_proyecto',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),  # Update the start date to today or an appropriate date
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Definir el DAG
with DAG(
    'Airflow_proyecto',
    default_args=default_args,
    description='workflow stadistics',
    schedule_interval='@daily',  # Set the schedule interval as per your requirements
) as dag:
    
    # Task 1: Extraer los datos de la base de datos
    extract_cardio = PythonOperator(
        task_id='extract_cardio',
        python_callable=extract_data_cardio,
    )

    transform_cardio = PythonOperator(
        task_id='transform_cardio',
        python_callable=transform_cardio_data,
    )

    extract_deaths = PythonOperator(
        task_id='extract_deaths',
        python_callable=extract_data_deaths,
    )

    Dimensional = PythonOperator(
        task_id='Dimensional',
        python_callable=load_data,
    )

    # Definir la secuencia de las tareas
    extract_cardio >> transform_cardio >> Dimensional
    extract_deaths >> Dimensional