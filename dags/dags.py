import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
from etl import extract_data, transform_cardio_data, transform_deaths_data, load_data

sys.path.append('/home/manuel/Escritorio/proyecto_ETL/ETL-1')

# Definir los argumentos por defecto para las tareas
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
with DAG(
    'ETL_Cardiovascular',
    default_args=default_args,
    description='ETL process for cardiovascular and death data',
    schedule_interval=timedelta(days=1),  # Configura el DAG para que se ejecute diariamente
    catchup=False,
) as dag:
    
    # Task 1: Extraer los datos de la base de datos
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        provide_context=True,  # Necesario para pasar los datos entre tareas
        dag=dag,
    )

    # Task 2: Transformar los datos de cardio
    transform_cardio_task = PythonOperator(
        task_id='transform_cardio_data',
        python_callable=transform_cardio_data,
        provide_context=True,  # Necesario para pasar los datos entre tareas
        dag=dag,
    )

    # Task 3: Transformar los datos de muertes
    transform_deaths_task = PythonOperator(
        task_id='transform_deaths_data',
        python_callable=transform_deaths_data,
        provide_context=True,  # Necesario para pasar los datos entre tareas
        dag=dag,
    )

    # Task 4: Cargar los datos transformados en la base de datos
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,  # Necesario para pasar los datos entre tareas
        dag=dag,
    )

    # Definir la secuencia de las tareas
    extract_task >> [transform_cardio_task, transform_deaths_task] >> load_task
