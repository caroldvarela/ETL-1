from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CardioTrain(Base):
    __tablename__ = 'CardioTrain'

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    ap_hi = Column(Integer, nullable=False)  # Presión arterial sistólica
    ap_lo = Column(Integer, nullable=False)  # Presión arterial diastólica
    cholesterol = Column(Integer, nullable=False)
    gluc = Column(Integer, nullable=False)
    smoke = Column(Integer, nullable=False)
    alco = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False)
    cardio = Column(Integer, nullable=False)

    def __str__(self):
        return f"table create"


class CauseOfDeaths(Base):
    __tablename__ = 'cause_of_deaths'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    cause = Column(String, nullable=False)
    deaths = Column(Integer, nullable=False)

    def __str__(self):
        return f"<CauseOfDeaths(id={self.id}, country={self.country}, year={self.year})>"
