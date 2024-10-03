import pandas as pd
import sys
import os
from dotenv import load_dotenv
from decouple import config

load_dotenv()
work_dir = os.getenv('WORK_DIR')


import pandas as pd
import os
import sys
from decouple import config
from sqlalchemy.orm import sessionmaker
from src.database.dbconnection import getconnection
from src.model.models import *

from transform.DimensionalModels import DimensionalModel
from transform.TransformData import DataTransform
from transform.TransformData import DataTransformCauseOfDeaths
import logging as log
from sqlalchemy.orm import sessionmaker, aliased
import json
from transform.TransformData import DataTransform, DataTransformCauseOfDeaths


def extract_data_cardio(**kwargs):
    engine = getconnection()
    Session = sessionmaker(bind=engine)
    session = Session()
    log.info("Starting data extraction")
    table = aliased(CardioTrain)
    query = str(session.query(table).statement)
    df = pd.read_sql(query, con=engine)
    log.info(f"Finish the data extraction {df}")
    kwargs['ti'].xcom_push(key='cardio', value=df.to_json(orient='records'))

    return df.to_json(orient='records')

def transform_cardio_data(**kwargs):
    log.info("Starting Data transform")
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids="extract_cardio", key='cardio')
    if str_data is None:
        log.error("No data found in XCom for 'cardio'")
        return

    json_df = json.loads(str_data)
    df = pd.json_normalize(data=json_df)
    log.info(f"Data is {df}")
    file = DataTransform(df)
    file.gender_by_category()
    file.cholesterol_by_category()
    file.gluc_by_category()
    file.bmi()
    file.days_to_age()
    file.StandardizeBloodPressure()
    file.CategorizeBMI()
    file.categorize_blood_pressure()
    file.CalculatePulsePressure()

    df = file.df.copy()


    result = {
        "source":"deaths",
        "data": df.to_dict(orient='records')
    }
    kwargs['ti'].xcom_push(key='transform_cardio_data', value=json.dumps(result))

    return json.dumps(result)




def extract_data_deaths(**kwargs):
    engine = getconnection()
    Session = sessionmaker(bind=engine)
    session = Session()
    log.info("Starting data extraction")
    table = aliased(CauseOfDeaths)
    query = str(session.query(table).statement)
    df = pd.read_sql(query, con=engine)
    log.info(f"Finish the data extraction {df}")

    result = {
        "source":"deaths",
        "data": df.to_dict(orient='records')
    }
    kwargs['ti'].xcom_push(key='deaths', value=json.dumps(result))

    return json.dumps(result)

def load_data(**kwargs):
    log.info("Starting data merge")

    ti = kwargs["ti"]
    
    # Pull data from XCom
    json_1 = ti.xcom_pull(task_ids="transform_cardio", key='transform_cardio_data')
    json_2 = ti.xcom_pull(task_ids="extract_deaths", key='deaths')

    log.info(json_1)
    # Check if the data exists
    if json_1 is None:
        log.error("No data found in XCom for 'transform_cardio'")
        return
    
    log.info(json_2)
    if json_2 is None:
        log.error("No data found in XCom for 'transform_deaths'")
        return
        
    data1 = json.loads(json_1)
    data2 = json.loads(json_2)


    df1 = pd.DataFrame(data1["data"])
    df2 = pd.DataFrame(data2["data"])

    DimensionalModel(df1,df2)

    return df1.to_json(orient='records')