from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

BASE = declarative_base()


class Staging(BASE):
    
    __tablename__ = 'Staging'
    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(float, nullable=False)
    ap_hi = Column(Integer, nullable=False)
    ap_lo = Column(Integer, nullable=False)
    cholesterol = Column(Integer, nullable=False)
    gluc = Column(Integer, nullable=False)
    smoke = Column(Integer, nullable=False)
    alco = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False)
    cardio = Column(Integer, nullable=False)
    
    def __str__ (self):
        return f" Table: {self.Staging.__table__}"