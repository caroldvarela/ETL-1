from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CardioTrain(Base):
    __tablename__ = 'cardio_train'

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    ap_hi = Column(Integer, nullable=False)  # Presión arterial sistólica
    ap_lo = Column(Integer, nullable=False)  # Presión arterial diastólica
    cholesterol = Column(Integer, nullable=False)
    gluc = Column(Integer, nullable=False)
    smoke = Column(Boolean, nullable=False)
    alco = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    cardio = Column(Boolean, nullable=False)

    def __str__(self):
        return f"<CardioTrain(id={self.id}, age={self.age}, gender={self.gender})>"


class CauseOfDeaths(Base):
    __tablename__ = 'cause_of_deaths'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    cause = Column(String, nullable=False)
    deaths = Column(Integer, nullable=False)

    def __str__(self):
        return f"<CauseOfDeaths(id={self.id}, country={self.country}, year={self.year})>"
