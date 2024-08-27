import pandas as pd
import numpy as np
from math import floor

class DataTransform:
    def __init__(self, file):

        self.df = pd.read_csv(file, sep=";")
    
    
    def  gender_by_category(self) -> None:
        self.gender_to_category = {
            1 : 'Female',
            2 : 'Male'
        }
        self.df['gender'] = self.df['gender'].map(self.gender_to_category)
    
    def cholesterol_by_category(self) -> None:
        self.cholesterol_to_category = {
            1: 'normal',
            2: 'above normal',
            3: 'well above normal'
        }
        self.df['cholesterol'] = self.df['cholesterol'].map(self.cholesterol_to_category)
    
    def gluc_by_category(self) -> None:

        self.gluc_to_category = {
            1: 'normal',
            2: 'above normal',
            3: 'well above normal'
        }
        self.df['gluc'] = self.df['gluc'].map(self.gluc_to_category)

    def bmi(self) -> None:

        self.df['bmi'] = round(self.df['weight'] / ((self.df['height']/100 )** 2), 2)
        self.df['bmi'] = self.df['bmi'].astype(float)

    def days_to_age(self) -> None:

        self.df['age'] = np.floor(self.df['age'] / 365.3)
        self.df['age'] = self.df['age'].astype(int)
        
    def nomalize_gluc(self) -> pd.DataFrame:

        unique_gluc = self.df['gluc'].unique()

        gluc_df = pd.DataFrame({
            'id': range(1, len(unique_gluc) + 1),
            'GlucLevel': unique_gluc
        })

        gluc_map = dict(zip(unique_gluc, gluc_df['id']))

        self.df['glucID'] = self.df['gluc'].map(gluc_map)

        self.df.drop(columns=['gluc'], inplace=True)

        return gluc_df
    
    
    def normalize_cholesterol(self) -> pd.DataFrame:

        unique_cholesterol = self.df['cholesterol'].unique()

        cholesterol_df = pd.DataFrame({
            'id': range(1, len(unique_cholesterol) + 1),
            'CholesterolLevel': unique_cholesterol
        })

        cholesterol_map = dict(zip(unique_cholesterol, cholesterol_df['id']))

        self.df['cholesterolID'] = self.df['cholesterol'].map(cholesterol_map)

        self.df.drop(columns=['cholesterol'], inplace=True)

        return cholesterol_df
    
    def StandardizeBloodPressure(self) -> None:
        self.df['ap_hi'] = self.df['ap_hi'].abs()
        self.df['ap_lo'] = self.df['ap_lo'].abs()
        self.df.drop(self.df[self.df["ap_hi"] < 80].index, inplace=True)
        self.df.drop(self.df[self.df["ap_hi"] > 250].index, inplace=True)
        self.df.drop(self.df[self.df["ap_lo"] < 50].index, inplace=True)
        self.df.drop(self.df[self.df["ap_lo"] > 150].index, inplace=True) 
        # Remove records where systolic equals diastolic
        self.df.drop(self.df[self.df["ap_hi"] == self.df["ap_lo"]].index, inplace=True)
      
    def CategorizeBMI(self) -> None:
        conditions = [
            (self.df["bmi"] <= 15),
            (self.df["bmi"] > 15) & (self.df["bmi"] <= 18.5),
            (self.df["bmi"] > 18.5) & (self.df["bmi"] <= 25),
            (self.df["bmi"] > 25) & (self.df["bmi"] <= 30),
            (self.df["bmi"] > 30) & (self.df["bmi"] <= 35),
            (self.df["bmi"] > 35) & (self.df["bmi"] <= 40),
            (self.df["bmi"] > 40)
        ]
        bmi_class = [0, 1, 2, 3, 4, 5, 6]
        self.df["bmi_class"] = np.select(conditions, bmi_class)
    
    def categorize_blood_pressure(self) -> None:

        systolic = self.df['ap_hi']
        diastolic = self.df['ap_lo']

        conditions = [
            (systolic < 120) & (diastolic < 80),
            (systolic < 130) & (diastolic < 85),
            ((systolic >= 130) & (systolic <= 139)) | ((diastolic >= 85) & (diastolic <= 89)),
            ((systolic >= 140) & (systolic <= 159)) | ((diastolic >= 90) & (diastolic <= 99)),
            ((systolic >= 160) & (systolic <= 179)) | ((diastolic >= 100) & (diastolic <= 109)),
            (systolic >= 180) | (diastolic >= 110),
            (systolic >= 140) & (systolic <= 160) & (diastolic < 90),
            (systolic > 160) & (diastolic < 90)
        ]

        bp_categories = [0, 1, 2, 3, 4, 5, 6, 7]

        self.df['bp_cat'] = np.select(conditions, bp_categories, default=-1)

    def  CalculatePulsePressure(self) -> None:
        self.df["pulse_press"] = self.df["ap_hi"] - self.df["ap_lo"]


    

class DataTransformCauseOfDeaths:
    def __init__(self, file):
        self.df = pd.read_csv(file, sep=",")

    def insert_id(self) -> None:
        """_summary_
        """
        self.df['id'] = range(1,len(self.df)+1)
        
    def drop_code(self) -> None:

        self.df.drop(columns=['Code'], inplace=True) 


    def total_deaths(self) -> None:


        self.df['TotalDeaths'] = self.df.iloc[:, 2:].sum(axis=1)

        first_columns = self.df.columns[:2]

        self.df = self.df[first_columns.tolist() + ['TotalDeaths'] + ['Cardiovascular']]


