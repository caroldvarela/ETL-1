import pandas as pd
import numpy as np
from math import floor

class DataTransform:
    def __init__(self, file_or_df):
        if isinstance(file_or_df, str): 
            self.df = pd.read_csv(file_or_df, sep=";")
        elif isinstance(file_or_df, pd.DataFrame):  
            self.df = file_or_df
        else:
            raise ValueError("The argument must be a URL/file path or a DataFrame.")
    
    
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
        bmi_class = ['Severely underweight', 'Underweight', 'Normal weight', 'Overweiht', 'Obesity class I', 'Obesity class II', 'Obesity class III']
        self.df["bmi_class"] = np.select(conditions, bmi_class)

    def categorize_blood_pressure(self) -> None:
        def classify_blood_pressure(row):
            if row['ap_hi'] < 120 and row['ap_lo'] < 80:
                return 'Normal'  # NORMAL
            elif 120 <= row['ap_hi'] <= 129 and row['ap_lo'] < 80:
                return 'Elevated'  # ELEVATED
            elif (130 <= row['ap_hi'] <= 139) or (80 <= row['ap_lo'] <= 89):
                return 'High Blood Pressure Stage 1'  # HIGH BLOOD PRESSURE STAGE 1
            elif (140 <= row['ap_hi'] <= 180) or (90 <= row['ap_lo'] <= 120):
                return 'High Blood Pressure Stage 2'  # HIGH BLOOD PRESSURE STAGE 2
            elif row['ap_hi'] > 180 or row['ap_lo'] > 120:
                return 'Hypertensive Crisis' # HYPERTENSIVE CRISIS
            else:
                return None 
        
        self.df['blood_pressure'] = self.df.apply(classify_blood_pressure, axis=1)
        self.df['blood_pressure'] = self.df['blood_pressure'].fillna('No one')
        if self.df['blood_pressure'].isnull().any():
            raise ValueError("There are still null values in 'blood_pressure' column.")


    def  CalculatePulsePressure(self) -> None:
        self.df["pulse_press"] = self.df["ap_hi"] - self.df["ap_lo"]
    
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

    def normalize_gender(self) -> pd.DataFrame:

        unique_gender = self.df['gender'].unique()

        gender_df = pd.DataFrame({
            'id': range(1, len(unique_gender) + 1),
            'gender': unique_gender
        })

        gender_map = dict(zip(unique_gender, gender_df['id']))

        self.df['genderID'] = self.df['gender'].map(gender_map)

        self.df.drop(columns=['gender'], inplace=True)

        return gender_df
    
    def normalize_bp(self) -> pd.DataFrame:

        unique_BP = self.df['blood_pressure'].unique()

        BP_df = pd.DataFrame({
            'id': range(1, len(unique_BP) + 1),
            'category': unique_BP
        })

        BP_map = dict(zip(unique_BP, BP_df['id']))

        self.df['BPCategoryId'] = self.df['blood_pressure'].map(BP_map)

        self.df.drop(columns=['blood_pressure'], inplace=True)

        return BP_df

    def normalize_bmi_class(self) -> pd.DataFrame:

        unique_bmi = self.df['bmi_class'].unique()

        bmi_df = pd.DataFrame({
            'id': range(1, len(unique_bmi) + 1),
            'category': unique_bmi
        })

        gender_map = dict(zip(unique_bmi, bmi_df['id']))

        self.df['bmi_classID'] = self.df['bmi_class'].map(gender_map)

        self.df.drop(columns=['bmi_class'], inplace=True)

        return bmi_df
    
    def normalize_lifestyle(self) -> pd.DataFrame:

        unique_lifestyle_df  = self.df[['smoke', 'alco','active']].drop_duplicates()

        lifestyle_df = pd.DataFrame({
            'id': range(1, len(unique_lifestyle_df) + 1),
            'smoke': unique_lifestyle_df['smoke'].values,
            'alco': unique_lifestyle_df['alco'].values,
            'active': unique_lifestyle_df['active'].values
        })

        lifestyle_map = {
            (row['smoke'], row['alco'], row['active']): row['id'] 
            for _, row in lifestyle_df.iterrows()
        }
        
        self.df['lifestyleID'] = self.df.apply(
            lambda row: lifestyle_map[(row['smoke'], row['alco'], row['active'])],
            axis=1
        )

        self.df.drop(columns=['smoke','alco','active'], inplace=True)

        return lifestyle_df

class DataTransformOwid:
    def __init__(self, file_or_df):
        if isinstance(file_or_df, str): 
            self.df = pd.read_csv(file_or_df)
        elif isinstance(file_or_df, pd.DataFrame):  
            self.df = file_or_df
        else:
            raise ValueError("error")
        
    def data_imputation(self):
        for col in self.df.columns:
            if col not in ['id', 'Country', 'Code', 'Year']:  
                self.df[col] = self.df.groupby('Year')[col].transform(lambda x: x.fillna(x.median()) if x.notna().sum() > 0 else x) #besity_prevalence_percentage & diabetes_prevalence_percentage just have information until 2016
    
    def feautres_imputation(self):
        self.df['gdp'] = self.df['gdp_per_capita']*self.df['population']
        self.df.insert(11, 'gdp', self.df.pop('gdp'))



class DataTransformCauseOfDeaths:
    def __init__(self, file_or_df):
        if isinstance(file_or_df, str): 
            self.df = pd.read_csv(file_or_df)
        elif isinstance(file_or_df, pd.DataFrame):  
            self.df = file_or_df
        else:
            raise ValueError("error")
    
    def insert_id(self) -> None:
        self.df['id'] = range(1,len(self.df)+1)
        
    def total_deaths(self) -> None:
        self.df['TotalDeaths'] = self.df.iloc[:, 3:].sum(axis=1)

        first_columns = self.df.columns[:3]


        self.df = self.df[first_columns.tolist()+ ['TotalDeaths']+ ['Cardiovascular']]

    
    def normalize_countries(self) -> pd.DataFrame:
        # Create a copy to avoid modifying a slice of the original DataFrame
        dfcopy = self.df.copy()

        unique_country_df = dfcopy[['Country', 'Code']].drop_duplicates()

        country_df = pd.DataFrame({
            'id': range(1, len(unique_country_df) + 1),
            'Country': unique_country_df['Country'].values,
            'Code': unique_country_df['Code'].values
        })

        country_map = dict(zip(unique_country_df['Country'], country_df['id']))

        # Use .loc to assign CountryID
        self.df.loc[:, 'CountryID'] = self.df['Country'].map(country_map)

        # Drop columns using inplace operation
        self.df.drop(columns=['Country', 'Code'], inplace=True)

        return country_df

    def normalize_year(self) -> pd.DataFrame:
        # Create a copy to avoid modifying a slice of the original DataFrame
        unique_year = self.df['Year'].unique()

        year_df = pd.DataFrame({
            'id': range(1, len(unique_year) + 1),
            'year': unique_year,
            'decade': (unique_year // 10) * 10
        })

        year_map = dict(zip(unique_year, year_df['id']))

        # Use .loc to assign YearID
        self.df.loc[:, 'YearID'] = self.df['Year'].map(year_map)

        # Drop columns using inplace operation
        self.df.drop(columns=['Year'], inplace=True)

        return year_df
