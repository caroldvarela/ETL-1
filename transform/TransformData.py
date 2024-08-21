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
            3: 'well'
        }
        self.df['gluc'] = self.df['gluc'].map(self.gluc_to_category)

    def IMC(self) -> None:

        self.df['IMC'] = round(self.df['weight'] / (self.df['height'] ** 2), 2)
        self.df['IMC'] = self.df['IMC'].astype(float)


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