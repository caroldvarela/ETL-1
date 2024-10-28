from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

BASE = declarative_base()
MAX_STRING_SIZE = 50

class CardioTrain(BASE):
    __tablename__ = 'CardioTrain'

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    ap_hi = Column(Integer, nullable=False)  # Systolic blood pressure.
    ap_lo = Column(Integer, nullable=False)  # Diastolic blood pressure.
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
    Country = Column(String(40), nullable=False)
    Code = Column(String(3), nullable=False)
    Year = Column(Integer, nullable=False)
    Cardiovascular = Column(Integer, nullable=False)
    TotalDeaths = Column(Integer, nullable=False)

    def __str__(self):
        return f"<CauseOfDeaths(id={self.id}, country={self.country}, year={self.year})>"

class CauseOfDeathsDimensional(BASE):
    __tablename__ = 'CauseOfDeathsDimensional'

    id = Column(Integer, primary_key=True, autoincrement=True)
    CountryID = Column(Integer, ForeignKey('Countries.id'), nullable=False)
    YearID = Column(Integer, ForeignKey('Year.id'), nullable=False)
    Cardiovascular = Column(Integer, nullable=False)
    nitrogen_oxide = Column(Float, nullable=False)
    sulphur_dioxide = Column(Float, nullable=False)
    carbon_monoxide = Column(Float, nullable=False)
    black_carbon = Column(Float, nullable=False)
    ammonia= Column(Float, nullable=False)
    non_methane_volatile_organic_compounds = Column(Float, nullable=False)
    gdp_per_capita = Column(Float, nullable=False)
    gdp = Column(Float, nullable=False)
    obesity_prevalence_percentage = Column(Float, nullable=True)
    diabetes_prevalence_percentage = Column(Float, nullable=True)
    population = Column(Float, nullable=False)
    DeathRate = Column(Float, nullable=False)
    TotalDeaths = Column(Integer, nullable=False)

    country = relationship("Countries", back_populates="causeofdeathsdimensional")
    year = relationship("Year", back_populates="causeofdeathsdimensional")

    def __str__(self):
        return f"<CauseOfDeaths(id={self.id}, country={self.country}, year={self.year})>"

class Countries(BASE):
    __tablename__ = 'Countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Country = Column(String(40), nullable=False)
    Code = Column(String(3), nullable=False)

    causeofdeathsdimensional = relationship("CauseOfDeathsDimensional", back_populates="country")

    def __str__(self):
        return f"<CauseOfDeaths(id={self.id})>"

class Year(BASE):
    __tablename__ = 'Year'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    decade = Column(Integer, nullable=False)

    causeofdeathsdimensional = relationship("CauseOfDeathsDimensional", back_populates="year")

    def __str__(self):
        return f"<CauseOfDeaths(id={self.id})>"


class CardioTrainNormalize(BASE):
    __tablename__ = 'CardioTrainNormalize'

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(MAX_STRING_SIZE), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    ap_hi = Column(Integer, nullable=False)  # Systolic blood pressure.
    ap_lo = Column(Integer, nullable=False)  # Diastolic blood pressure.
    cholesterol = Column(String, nullable=False)
    gluc = Column(String, nullable=False)
    smoke = Column(Integer, nullable=False)
    alco = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False)
    bmi_class = Column(String(MAX_STRING_SIZE), nullable=False)
    blood_pressure = Column(String(MAX_STRING_SIZE), nullable=False)
    pulse_press = Column(Integer, nullable=False)
    cardio = Column(Integer, nullable=False)


    def __str__(self):
        return f"table create"


class CardioTrainNormalizeDimensional(BASE):
    __tablename__ = 'CardioTrainNormalizeDimensional'

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    genderID = Column(Integer, ForeignKey('Gender.id'), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    ap_hi = Column(Integer, nullable=False)  # Systolic blood pressure.
    ap_lo = Column(Integer, nullable=False)  # Diastolic blood pressure.
    cholesterolID = Column(Integer, ForeignKey('CholesterolTypes.id'), nullable=False)
    glucID = Column(Integer, ForeignKey('GlucoseTypes.id'), nullable=False)
    lifestyleID = Column(Integer, ForeignKey('LifeStyle.id'), nullable=False)
    bmi_classID = Column(Integer, ForeignKey('BMIClass.id'), nullable=False)
    pulse_press = Column(Integer, nullable=False)
    BPCategoryId = Column(Integer, ForeignKey('BloodPreasureCategories.id'), nullable=False)
    cardio = Column(Integer, nullable=False)

    gender = relationship("Gender", back_populates="cardio_dimensional")
    cholesterol = relationship("CholesterolTypes", back_populates="cardio_dimensional")
    glucose = relationship("GlucoseTypes", back_populates="cardio_dimensional")
    lifestyle = relationship("LifeStyle", back_populates="cardio_dimensional")
    bmiclass = relationship("BMIClass", back_populates="cardio_dimensional")
    bp_categorie = relationship("BloodPreasureCategories", back_populates="cardio_dimensional")

    def __str__(self):
        return f"table create"

class Gender(BASE):
    __tablename__ = 'Gender'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(String(MAX_STRING_SIZE), nullable=False)
    
    cardio_dimensional = relationship("CardioTrainNormalizeDimensional", back_populates="gender")

    def __str__ (self):
        return f" Table: {self.Gender.__table__}"

class CholesterolTypes(BASE):
    __tablename__ = 'CholesterolTypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    CholesterolLevel = Column(String(MAX_STRING_SIZE), nullable=False)

    
    cardio_dimensional = relationship("CardioTrainNormalizeDimensional", back_populates="cholesterol")

    def __str__ (self):
        return f" Table: {self.CholesterolTypes.__table__}"

class GlucoseTypes(BASE):
    __tablename__ = 'GlucoseTypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    GlucLevel = Column(String(MAX_STRING_SIZE), nullable=False)
    
    
    cardio_dimensional = relationship("CardioTrainNormalizeDimensional", back_populates="glucose")

    def __str__ (self):
        return f" Table: {self.GlucoseTypes.__table__}"

class LifeStyle(BASE):
    __tablename__ = 'LifeStyle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    smoke = Column(Integer, nullable=False)
    alco = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False)
    
    cardio_dimensional = relationship("CardioTrainNormalizeDimensional", back_populates="lifestyle")

    def __str__ (self):
        return f" Table: {self.LifeStyle.__table__}"

class BMIClass(BASE):
    __tablename__ = 'BMIClass'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(MAX_STRING_SIZE), nullable=False)
    
    cardio_dimensional = relationship("CardioTrainNormalizeDimensional", back_populates="bmiclass")

    def __str__ (self):
        return f" Table: {self.BMI.__table__}"

class BloodPreasureCategories(BASE):
    __tablename__ = 'BloodPreasureCategories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(MAX_STRING_SIZE), nullable=False)
    
    cardio_dimensional = relationship("CardioTrainNormalizeDimensional", back_populates="bp_categorie")

    def __str__ (self):
        return f" Table: {self.BloodPreasureCategories.__table__}"
