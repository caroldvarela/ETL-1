import os
import sys

work_dir = os.getenv("WORK_DIR")
sys.path.append(work_dir)

import pandas as pd
from transform.TransformData import *
from src.database.createTable import *
from src.model.models import *
from src.database.dbconnection import getconnection
from sqlalchemy.orm import sessionmaker

def DimensionalModel(dfCardio, dfDeaths):

    # Get engine from sqlalchemy
    engine = getconnection()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create Tables from Cardio dimension

    CreateTableCardio(BloodPreasureCategories, 'BloodPreasureCategories', engine)
    CreateTableCardio(BMIClass, 'BMIClass', engine)
    CreateTableCardio(LifeStyle, 'LifeStyle', engine)
    CreateTableCardio(GlucoseTypes, 'GlucoseTypes', engine)
    CreateTableCardio(CholesterolTypes, 'CholesterolTypes', engine)
    CreateTableCardio(Gender, 'Gender', engine)
    CreateTableCardio(CardioTrainNormalizeDimensional, 'CardioTrainNormalizeDimensional', engine)

    # Transformations

    fileCardio = DataTransform(dfCardio)
    
    # Create Dimensions

    transform_gluc = fileCardio.nomalize_gluc()
    transform_cholesterol = fileCardio.normalize_cholesterol()
    transform_gender = fileCardio.normalize_gender()
    transform_bp_class = fileCardio.normalize_bp()
    transform_bmi_class = fileCardio.normalize_bmi_class()
    transform_lifestyle = fileCardio.normalize_lifestyle()
    

    # Save the data into the tables
    transform_gluc.to_sql('GlucoseTypes', con=engine, if_exists='append', index=False)
    transform_cholesterol.to_sql('CholesterolTypes', con=engine, if_exists='append', index=False)
    transform_gender.to_sql('Gender', con=engine, if_exists='append', index=False)
    transform_bp_class.to_sql('BloodPreasureCategories', con=engine, if_exists='append', index=False)
    transform_bmi_class.to_sql('BMIClass', con=engine, if_exists='append', index=False)
    transform_lifestyle.to_sql('LifeStyle', con=engine, if_exists='append', index=False)

    fileCardio.df.to_sql('CardioTrainNormalizeDimensional', con=engine, if_exists='append', index=False)


    # Cause of deaths dimensional

    CreateTableDeaths(Year, 'Year', engine)
    CreateTableDeaths(Countries, 'Countries', engine)
    CreateTableDeaths(CauseOfDeathsDimensional, 'CauseOfDeathsDimensional', engine)

    fileDeaths = DataTransformCauseOfDeaths(dfDeaths)

    transform_countries = fileDeaths.normalize_countries()
    transform_year = fileDeaths.normalize_year()
    

    transform_countries.to_sql('Countries', con=engine, if_exists='append', index=False)
    transform_year.to_sql('Year', con=engine, if_exists='append', index=False)

    fileDeaths.df.to_sql('CauseOfDeathsDimensional', con=engine, if_exists='append', index=False)

    return fileCardio.df, fileDeaths.df

