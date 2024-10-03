import os
import sys

work_dir = os.getenv("WORK_DIR")
sys.path.append(work_dir)

import pandas as pd
from src.model.models import CardioTrain, CauseOfDeaths
from src.database.dbconnection import getconnection
from sqlalchemy import inspect, create_engine # added create_engine
from sqlalchemy.exc import SQLAlchemyError
from transform.TransformData import DataTransformCauseOfDeaths


def create_tables():
    engine = getconnection()

    try:
        # Drop tables if they exist
        if inspect(engine).has_table('CardioTrain'):
            CardioTrain.__table__.drop(engine)
            print("CardioTrain table dropped.")
        if inspect(engine).has_table('CauseOfDeaths'):
            CauseOfDeaths.__table__.drop(engine)
            print("CauseOfDeaths table dropped.")

        # Create tables
        CardioTrain.__table__.create(engine)
        print("CardioTrain table created successfully.")
        CauseOfDeaths.__table__.create(engine)
        print("CauseOfDeaths table created successfully.")

        # Load data
        try:
            df_cardio = pd.read_csv('data/cardio_train.csv', sep=";") # Changed to relative path
            df_cardio.to_sql('CardioTrain', engine, if_exists='append', index=False)
            print("CardioTrain data loaded.")
        except FileNotFoundError:
            print("cardio_train.csv not found. CardioTrain table created but not populated.")
        except Exception as e:
            print(f"Error loading CardioTrain data: {e}")

        try:
            df_deaths = pd.read_csv('data/cause_of_deaths.csv')

            transformer = DataTransformCauseOfDeaths(df_deaths)
            transformer.total_deaths()  # Calculate TotalDeaths
            transformer.insert_id()  # Insert ID

            # Select only the required columns for CauseOfDeaths
            df_deaths = transformer.df[['id', 'Country', 'Code', 'Year', 'Cardiovascular', 'TotalDeaths']]

            df_deaths.rename(columns={
                'country': 'country',
                'code': 'code',
                'year': 'year',
                'cardiovascular': 'cardiovascular',
                'totalDeaths': 'total_deaths'
            }, inplace=True)

            df_deaths.to_sql('CauseOfDeaths', engine, if_exists='append', index=False)
            print("CauseOfDeaths data loaded.")
        except FileNotFoundError:
            print("cause_of_deaths.csv not found. CauseOfDeaths table created but not populated.")
        except Exception as e:
            print(f"Error loading and transforming CauseOfDeaths data: {e}")
      


        except FileNotFoundError:
            print("cause_of_deaths.csv not found. CauseOfDeaths table created but not populated.")
        except Exception as e:
            print(f"Error loading CauseOfDeaths data: {e}")

    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    create_tables()