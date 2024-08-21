from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

BASE = declarative_base()
MAX_STRING_SIZE = 20

class CardioTrain(BASE):
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


class CauseOfDeaths(BASE):
    __tablename__ = 'CauseOfDeaths'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    cause = Column(String, nullable=False)
    deaths = Column(Integer, nullable=False)

    def __str__(self):
        return f"<CauseOfDeaths(id={self.id}, country={self.country}, year={self.year})>"


class CardioTrainNormalize(BASE):
    __tablename__ = 'CardioTrainNormalize'

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(MAX_STRING_SIZE), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    IMC = Column(Float, nullable=False)
    ap_hi = Column(Integer, nullable=False)  # Presión arterial sistólica
    ap_lo = Column(Integer, nullable=False)  # Presión arterial diastólica
    cholesterolID = Column(Integer, ForeignKey('CholesterolTypes.id'), nullable=False)
    glucID = Column(Integer, ForeignKey('GlucoseTypes.id'), nullable=False)
    smoke = Column(Integer, nullable=False)
    alco = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False)
    cardio = Column(Integer, nullable=False)

    cholesterol = relationship("CholesterolTypes", back_populates="cardio")
    glucose = relationship("GlucoseTypes", back_populates="cardio")

    def __str__(self):
        return f"table create"


class CholesterolTypes(BASE):
    __tablename__ = 'CholesterolTypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    CholesterolLevel = Column(String(MAX_STRING_SIZE), nullable=False)
    
    cardio = relationship("CardioTrainNormalize", back_populates="cholesterol")

    def __str__ (self):
        return f" Table: {self.Countries.__table__}"

class GlucoseTypes(BASE):
    __tablename__ = 'GlucoseTypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    GlucLevel = Column(String(MAX_STRING_SIZE), nullable=False)
    
    cardio = relationship("CardioTrainNormalize", back_populates="glucose")

    def __str__ (self):
        return f" Table: {self.Countries.__table__}"
    

