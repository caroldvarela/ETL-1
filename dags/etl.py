import pandas as pd
import os
import sys
from decouple import config
from sqlalchemy.orm import sessionmaker
from src.database.dbconnection import getconnection
from transform.DimensionalModels import DimensionalModel
from transform.TransformData import DataTransform
from transform.TransformData import DataTransformCauseOfDeaths
import logging as log

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))


def extract_data(**kwargs):
    log.info("Extracting data from the database")
    
    # Obtener la conexión
    engine = getconnection()
    
    # Leer datos de las tablas en DataFrames
    try:
        df_cardio = pd.read_sql('SELECT * FROM "CardioTrain"', con=engine)
        df_deaths = pd.read_sql('SELECT * FROM "CauseOfDeaths"', con=engine)
        log.info("Data extracted successfully")
    except Exception as e:
        log.error(f"Error extracting data: {e}")
        raise
    
    # Empujar datos usando XCom
    kwargs['ti'].xcom_push(key='cardio_data', value=df_cardio.to_json(orient='records'))
    kwargs['ti'].xcom_push(key='deaths_data', value=df_deaths.to_json(orient='records'))

def transform_cardio_data(**kwargs):
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids='extract_data', key='cardio_data')
    
    if str_data:
        df_cardio = pd.read_json(str_data, orient='records')
        log.info("Transforming cardiovascular data")
        
        # Llamar a las funciones de transformación de cardio
        try:
            transformed_data = DataTransform(df_cardio)
            transformed_data.gender_by_category()
            transformed_data.bmi()
            transformed_data.CategorizeBMI()
            log.info("Cardiovascular data transformed successfully")
        except Exception as e:
            log.error(f"Error transforming cardiovascular data: {e}")
            raise
        
        df_transformed = transformed_data.df
        kwargs['ti'].xcom_push(key='transformed_cardio_data', value=df_transformed.to_json(orient='records'))
    else:
        log.error("No cardiovascular data found in XCom")

def transform_deaths_data(**kwargs):
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids='extract_data', key='deaths_data')

    if str_data:
        df_deaths = pd.read_json(str_data, orient='records')
        log.info("Transforming cause of death data")
        
        # Llamar a las funciones de transformación de muertes
        try:
            transformed_deaths = DataTransformCauseOfDeaths(df_deaths)
            transformed_deaths.total_deaths()
            log.info("Cause of death data transformed successfully")
        except Exception as e:
            log.error(f"Error transforming cause of death data: {e}")
            raise
        
        df_transformed = transformed_deaths.df
        kwargs['ti'].xcom_push(key='transformed_deaths_data', value=df_transformed.to_json(orient='records'))
    else:
        log.error("No cause of death data found in XCom")

def load_data(**kwargs):
    ti = kwargs['ti']
    cardio_data = ti.xcom_pull(task_ids='transform_cardio_data', key='transformed_cardio_data')
    deaths_data = ti.xcom_pull(task_ids='transform_deaths_data', key='transformed_deaths_data')

    if cardio_data and deaths_data:
        log.info("Loading data into the database")
        try:
            engine = getconnection()
            DimensionalModel(pd.read_json(cardio_data), pd.read_json(deaths_data))
            log.info("Data loaded into the database successfully")
        except Exception as e:
            log.error(f"Error loading data into the database: {e}")
            raise
    else:
        log.error("No transformed data found for loading")
