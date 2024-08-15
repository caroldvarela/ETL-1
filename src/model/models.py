from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

BASE = declarative_base()
MAX_STRING_SIZE = 100

class Staging(BASE):
    
    __tablename__ = 'Staging'
    id = Column(Integer, primary_key=True, autoincrement=True)
    WorkYear = Column(Integer, nullable=False)
    ExperienceLevel = Column(String(MAX_STRING_SIZE), nullable=False)
    EmploymentType = Column(String(MAX_STRING_SIZE), nullable=False)
    JobTitle = Column(String(MAX_STRING_SIZE), nullable=False)
    Salary =  Column(Integer, primary_key=True, autoincrement=True)
    SalaryCurrency = Column(String(MAX_STRING_SIZE), nullable=False)
    SalaryInUSD =  Column(Integer, primary_key=True, autoincrement=True)
    EmployeeResidence = Column(String(MAX_STRING_SIZE), nullable=False)
    RemoteRatio =  Column(Integer, primary_key=True, autoincrement=True)
    CompanyLocation = Column(String(MAX_STRING_SIZE), nullable=False)
    CompanySize = Column(String(MAX_STRING_SIZE), nullable=False)

    def __str__ (self):
        return f" Table: {self.Staging.__table__}"