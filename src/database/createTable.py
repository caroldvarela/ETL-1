from sqlalchemy import inspect

from sqlalchemy.exc import SQLAlchemyError
from ..model.models import CardioTrainNormalize, CauseOfDeaths

def CreateTableCardio(table,tableName, engine):
    try:
        if inspect(engine).has_table(tableName):
            if inspect(engine).has_table('CardioTrainNormalize'):
                CardioTrainNormalize.__table__.drop(engine)
            table.__table__.drop(engine, checkfirst=True)
        table.__table__.create(engine)
        print(f"Table {tableName} created successfully.")
    except SQLAlchemyError as e:
        print(f"Error creating table: {e}")
    finally:
        engine.dispose()



def CreateTableDeaths(table,tableName, engine):
    try:
        if inspect(engine).has_table(tableName):
            if inspect(engine).has_table('CauseOfDeaths'):
                CauseOfDeaths.__table__.drop(engine)
            table.__table__.drop(engine, checkfirst=True)
        table.__table__.create(engine)
        print(f"Table {tableName} created successfully.")
    except SQLAlchemyError as e:
        print(f"Error creating table: {e}")
    finally:
        engine.dispose()