import os
import sys
import pandas as pd
from dotenv import load_dotenv
from decouple import config
from transform.charts import get_data
import great_expectations as gx
import great_expectations.expectations as gxe


load_dotenv()
work_dir = os.getenv('WORK_DIR')



from sqlalchemy.orm import sessionmaker
from src.database.dbconnection import getconnection
from src.model.models import *

from src.database.createTable import CreateTableCardio, CreateTableDeaths

from transform.DimensionalModels import DimensionalModel
from transform.TransformData import *

import logging as log
from sqlalchemy.orm import sessionmaker, aliased
import json
from transform.TransformData import DataTransform, DataTransformCauseOfDeaths

from src.streaming.kafka_utils import kafka_producer
from src.gx_utils.validation import validate_cardio_data, validate_deaths_data, validate_api_data



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

def validate_cardio(**kwargs):
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids="extract_cardio", key='cardio')
    json_df = json.loads(str_data)
    df = pd.json_normalize(data=json_df)
    
    validate_cardio_data(df)  
    kwargs['ti'].xcom_push(key='cardio_validate', value=df.to_json(orient='records'))
    return df.to_json(orient='records')


def transform_cardio_data(**kwargs):
    log.info("Starting Data transform")
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids="validate_cardio_data", key='cardio_validate')
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



def extract_owid_data(**kwargs):
    air_pollution = get_data('https://ourworldindata.org/grapher/long-run-air-pollution')
    air_pollution.rename(columns={'entities': 'Country', 'years': 'Year', 'nox': 'nitrogen_oxide(NOx)' , 'so2': 'sulphur_dioxide(SO2)', 'co': 'carbon_monoxide(CO)', 'bc': 'black_carbon(BC)', 'nh3': 'ammonia(NH3)', 'nmvoc': 'non_methane_volatile_organic_compounds'}, inplace=True)

    gdp_per_capita = get_data('https://ourworldindata.org/grapher/gdp-per-capita-penn-world-table')
    gdp_per_capita.rename(columns={'entities': 'Country', 'years': 'Year','gdp_per_capita_penn_world_table': 'gdp_per_capita'}, inplace=True)

    obesity = get_data('https://ourworldindata.org/grapher/obesity-prevalence-adults-who-gho')
    obesity.rename(columns={'entities': 'Country', 'years': 'Year', 'obesity_prevalence_adults_who_gho': 'obesity_prevalence_percentage'}, inplace=True)

    diabetes = get_data('https://ourworldindata.org/grapher/diabetes-prevalence-who-gho')
    diabetes.rename(columns={'entities': 'Country', 'years': 'Year', 'diabetes_prevalence_who_gho': 'diabetes_prevalence_percentage'}, inplace=True)

    population = get_data('https://ourworldindata.org/grapher/population')
    population.rename(columns={'entities': 'Country', 'years': 'Year'}, inplace=True)

    merged_air = pd.merge(air_pollution, gdp_per_capita, left_on=['Country', 'Year'],
                        right_on=['Country', 'Year'], how='left')
    merged_obsity = pd.merge(merged_air, obesity, left_on=['Country', 'Year'],
                        right_on=['Country', 'Year'], how='left')
    merged_diabetes = pd.merge(merged_obsity, diabetes, left_on=['Country', 'Year'],
                        right_on=['Country', 'Year'], how='left')
    merged_df = pd.merge(merged_diabetes, population, left_on=['Country', 'Year'],
                        right_on=['Country', 'Year'], how='left')
    
    merged_df = merged_df.sort_values(by=['Country', 'Year'], ascending=[True, True])

    kwargs['ti'].xcom_push(key='owid', value=merged_df.to_json(orient='records'))

    return merged_df.to_json(orient='records')

def validate_api(**kwargs):
    log.info("Starting Data API validate")
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids="extract_api", key='owid')
    if str_data is None:
        log.error("No data found in XCom for 'owid'")
        return
    json_df = json.loads(str_data)
    df = pd.json_normalize(data=json_df)
    
    
    df = df[(df["Year"] >= 1990) & (df["Year"] <= 2019)]
    
    
    df['gdp_per_capita'].fillna(df['gdp_per_capita'].median(), inplace=True)
    df['obesity_prevalence_percentage'].fillna(df['obesity_prevalence_percentage'].median(), inplace=True)
    df['diabetes_prevalence_percentage'].fillna(df['diabetes_prevalence_percentage'].median(), inplace=True)
    
   
    expected_columns = [
        "Country", "Code", "Year", "CardiovascularDeaths", "nitrogen_oxide(NOx)",
        "sulphur_dioxide(SO2)", "carbon_monoxide(CO)", "black_carbon(BC)", 
        "ammonia(NH3)", "non_methane_volatile_organic_compounds", "gdp_per_capita",
        "obesity_prevalence_percentage", "diabetes_prevalence_percentage", 
        "population", "TotalDeaths"
    ]
    df = df.reindex(columns=expected_columns)
    
    # Validation with Great Expectations
    kwargs['ti'].xcom_push(key='owid_validate', value=df.to_json(orient='records'))
    validate_api_data(df)
    return df.to_json(orient='records')




def transform_owid(**kwargs):
    log.info("Starting Data transform")
    ti = kwargs['ti']
    str_data = ti.xcom_pull(task_ids="validate_api_data", key='owid_validate')
    if str_data is None:
        log.error("No data found in XCom for 'cardio'")
        return
    json_df = json.loads(str_data)
    df = pd.json_normalize(data=json_df)
    file = DataTransformOwid(df)

    file.feautres_imputation()
  
    rename_columns = {
        'nitrogen_oxide(NOx)': 'nitrogen_oxide',
        'sulphur_dioxide(SO2)': 'sulphur_dioxide',
        'carbon_monoxide(CO)': 'carbon_monoxide',
        'black_carbon(BC)': 'black_carbon',
        'ammonia(NH3)': 'ammonia'
    }

    df = file.df
    df = df.rename(columns=rename_columns)

    result = {
        "source":"owid_transform",
        "data": df.to_dict(orient='records')
    }

    kwargs['ti'].xcom_push(key='owidtransform', value=json.dumps(result))

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


def validate_deaths(**kwargs):
    ti = kwargs['ti']
    json_data = ti.xcom_pull(task_ids="extract_deaths", key='deaths')
    data = json.loads(json_data)
    df = pd.DataFrame(data["data"])
    
    validate_deaths_data(df)  # Call to validation from gx_utils

    result = {
            "source":"deaths",
            "data": df.to_dict(orient='records')
    }
    kwargs['ti'].xcom_push(key='deaths_validated', value=json.dumps(result))

    return json.dumps(result)





def merge(**kwargs):
    log.info("Starting data merge")
    # Pull data from XCom
    ti = kwargs["ti"]
    json_2 = ti.xcom_pull(task_ids="transform_api", key='owidtransform')
    json_1 = ti.xcom_pull(task_ids="validate_deaths_data", key='deaths_validated')
    
    # Check if json_1 and json_2 are valid
    if json_1 is None:
        log.error("No data found in XCom for 'transform_cardio'")
        return
    
    if json_2 is None:
        log.error("No data found in XCom for 'transform_deaths'")
        return

    # Load the data as JSON
    data1 = json.loads(json_1)
    data2 = json.loads(json_2)

    # Ensure that data1 and data2 have the 'data' key
    if not isinstance(data1, dict) or "data" not in data1:
        log.error(f"Unexpected structure for data1: {data1}")
        return

    if not isinstance(data2, dict) or "data" not in data2:
        log.error(f"Unexpected structure for data2: {data2}")
        return
    
    
    df1 = pd.DataFrame(data1["data"])
    df2 = pd.DataFrame(data2["data"])

    log.info(df1.columns)
    log.info(df2.columns)

    df2.drop(columns=["Code", "CardiovascularDeaths", "TotalDeaths"], inplace=True)
    
    # Perform the merge and manipulation as before
    merged_df = pd.merge(df1, df2, left_on=['Country', 'Year'], right_on=['Country', 'Year'], how='left')
    
    log.info("Data merged successfully")
    log.info(merged_df.isnull().sum())
    log.info(merged_df.columns)
    
    for col in merged_df.columns:
        if col not in ['id', 'Country', 'Code', 'Year']:  
            merged_df[col] = merged_df.groupby('Year')[col].transform(lambda x: x.fillna(x.median()) if x.notna().sum() > 0 else x)

    merged_df['DeathRate'] = (merged_df['Cardiovascular'] / merged_df['population']) * 100000
    
    result = {
        "source": "merge_data",
        "data": merged_df.to_dict(orient='records')
    }
    
    kwargs['ti'].xcom_push(key='data_merged', value=json.dumps(result))

    return json.dumps(result)



def load_data(**kwargs):
    log.info("Starting data load")

    ti = kwargs["ti"]
    
    # Pull data from XCom
    json_2 = ti.xcom_pull(task_ids="Merge", key='data_merged')
    json_1 = ti.xcom_pull(task_ids="transform_cardio", key='transform_cardio_data')

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

    df2['obesity_prevalence_percentage'] = df2['obesity_prevalence_percentage'].fillna(df2['obesity_prevalence_percentage'].mean())
    df2['diabetes_prevalence_percentage'] = df2['diabetes_prevalence_percentage'].fillna(df2['diabetes_prevalence_percentage'].mean())

    df2_copy = df2.copy()

    df1_normalize, df2_normalize = DimensionalModel(df1,df2)


    result = {
        "data_cardio": df1_normalize.to_dict(orient='records'),
        "data_deaths": df2_copy.to_dict(orient='records')
    }

    kwargs['ti'].xcom_push(key='data_load', value=json.dumps(result))

    return json.dumps(result)


def producer_kafka(**kwargs):
    log.info("kafka producer")
    ti = kwargs["ti"]

    json1 = ti.xcom_pull(task_ids="load", key='data_load')
    data = json.loads(json1)
    df1 = pd.DataFrame(data["data_deaths"])
    
    kafka_producer(df1)
    log.info("All messages send")