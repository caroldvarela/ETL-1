from dotenv import load_dotenv
import os
import sys

load_dotenv()
work_dir = os.getenv('WORK_DIR')
sys.path.append(work_dir)





from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from datetime import datetime
from dags.etl import *



# Define default arguments for tasks
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

# Define the DAG
with DAG(
    'Airflow_proyecto',
    default_args=default_args,
    description='workflow stadistics',
    schedule_interval='@daily',  # Set the schedule interval as per your requirements
) as dag:
    
    # Task 1: Extract data from the database.
    extract_cardio = PythonOperator(
        task_id='extract_cardio',
        python_callable=extract_data_cardio,
    )
    # Task 2: Transform cardiovascular data
    transform_cardio = PythonOperator(
        task_id='transform_cardio',
        python_callable=transform_cardio_data,
    )
    # Task 3: Extract death data
    extract_deaths = PythonOperator(
        task_id='extract_deaths',
        python_callable=extract_data_deaths,
    )
    extract_api = PythonOperator(
        task_id='extract_api',
        python_callable=extract_owid_data,
    )
    transform_api = PythonOperator(
        task_id='transform_api',
        python_callable=transform_owid,
    )
    Merge = PythonOperator(
        task_id='Merge',
        python_callable=merge,
    )

    # Task 4: Load dimensional data
    load = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )

    producer = PythonOperator(
        task_id='producer',
        python_callable=producer_kafka,
    )

    

    # Define the sequence of tasks.
    extract_cardio >> transform_cardio >> load
    extract_deaths >> Merge >> load 
    extract_api >> transform_api >> Merge >> load
