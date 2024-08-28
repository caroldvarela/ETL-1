# ETL Project - First delivery 

Presented by 
- Jhonatan Steven Morales Hernandez: jhonatan.morales@uao.edu.co
- Carol Dayana Varela Cortez: carol.varela@uao.edu.co
- Manuel Alejandro Gruezo manuel.gruezo@uao.edu.co

## 📝 Introduction

Exploratory Data Analysis (EDA) is a crucial step in any data science project, as it allows us to better understand the structure, relationships, and patterns within the data before conducting any advanced modeling or analysis.

In this project, we will work with two main datasets:

1. **💓 Cardio Train Dataset**: This dataset contains information on various health indicators of individuals, such as age, gender, height, weight, blood pressure, cholesterol levels, and more. The goal is to explore these data points to identify potential correlations and patterns that could be useful in predicting cardiovascular diseases.

#### Data Description

The dataset is composed of three types of input features:

- *Objective*: Factual information.
- *Examination*: Results from medical examinations.
- *Subjective*: Information provided by the patient.

| Feature                    | Variable Type         | Variable      | Value Type                                                   |
|----------------------------|-----------------------|---------------|---------------------------------------------------------------|
| Age                        | Objective Feature     | age           | int (days)                                                   |
| Height                     | Objective Feature     | height        | int (cm)                                                     |
| Weight                     | Objective Feature     | weight        | float (kg)                                                   |
| Gender                     | Objective Feature     | gender        | categorical code                                             |
| Systolic Blood Pressure    | Examination Feature   | ap_hi         | int                                                          |
| Diastolic Blood Pressure   | Examination Feature   | ap_lo         | int                                                          |
| Cholesterol                | Examination Feature   | cholesterol   | 1: normal, 2: above normal, 3: well above normal             |
| Glucose                    | Examination Feature   | gluc          | 1: normal, 2: above normal, 3: well above normal             |
| Smoking                    | Subjective Feature    | smoke         | binary                                                       |
| Alcohol Intake             | Subjective Feature    | alco          | binary                                                       |
| Physical Activity          | Subjective Feature    | active        | binary                                                       |
| Cardiovascular Disease     | Target Variable       | cardio        | binary                                                       |

All dataset values were collected at the time of the medical examination.

### 🎯 Objectives of the ETL

- **📊 Understanding Data Distribution**: Analyze the distribution of individual variables to identify outliers, missing values, and understand the nature of the data.
- **🔗 Exploring Relationships Between Variables**: Investigate possible correlations between different variables that might be useful for subsequent modeling.
- **🔍 Identifying Patterns and Trends**: Search for patterns and trends in the data that could reveal relevant information for the project’s objectives.
- **🛠️ Data Preparation**: Perform the necessary transformations to clean and prepare the data for analysis and modeling.

### Tools used

- **Python** <img src="https://cdn-icons-png.flaticon.com/128/3098/3098090.png" alt="Python" width="21px" height="21px">
- **Jupyter Notebooks** <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" alt="Jupyer" width="21px" height="21px">
- **PostgreSQL** <img src="https://cdn-icons-png.flaticon.com/128/5968/5968342.png" alt="Postgres" width="21px" height="21px">
- **Power BI** <img src="https://1000logos.net/wp-content/uploads/2022/08/Microsoft-Power-BI-Logo.png" alt="PowerBI" width="30px" height="21px">
- **SQLAlchemy** <img src="https://quintagroup.com/cms/python/images/sqlalchemy-logo.png/@@images/eca35254-a2db-47a8-850b-2678f7f8bc09.png" alt="SQLalchemy" width="50px" height="21px">

### Repository Organization

- **data:** This folder contains all the csv files 'cardio_train.csv' and 'cause_of_deaths.csv'
- **notebooks:** This folder contains the exploratory data analysis and contains the notebook responsible for uploading the data.
- **src:** This folder contains the code responsible for connecting to our database, as well as the models of the tables that we already mentioned.

### Requirements
1. Install Python : [Python Downloads](https://www.python.org/downloads/)
2. Install PostgreSQL : [PostgreSQL Downloads](https://www.postgresql.org/download/)
3. Install Power BI : [Install Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494) 

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file
(add the file to the root of the project)

`PGDIALECT` <- This variable specifies the dialect of PostgreSQL to be used in the connection.  
`PGUSER` <- Defines the username to be used for authenticating against the PostgreSQL database.  
`PGPASSWD` <- This variable stores the password associated with the PostgreSQL user for authentication.  
`PGHOST` <- Indicates the address of the PostgreSQL database server that the application will connect to.  
`PGPORT` <-  Specifies the port on which the PostgreSQL database server is listening.  
`PGDB` <- Defines the name of the database that the application will connect to.  
`WORK_DIR` <- Sets the working directory for the application, indicating the base path for performing operations and managing files.

## Notebooks


### 1. Data Migration

- **File:** `Data_Setup.ipynb`
- **Description:** Imports the CSV file, transforms it, and migrates it to a relational PostgreSQL database using SQLAlchemy. In this step, the necessary tables are also created in the database.

### 2. Exploratory Data Analysis (EDA)

- **File:** `EDA.ipynb`
- **Description:** Performs exploratory analysis of the data loaded into the database. This includes identifying null values, reviewing data types, analyzing data distribution, and searching for patterns and correlations.

### 3. Data Transformation

- **File:** `Data_transformation.ipynb`
- **Description:** Performs deeper data transformation, such as creating new columns (e.g., the `Hired` column) and categorizing technologies. The transformed data is loaded back into the database.

## Setting Up the Environment

1. Clone this repository:

    ```bash
    git clone https://github.com/alej0909/ETL-1.git
    cd ETL-1
    ```

2. Create the database:

    ```sql
    CREATE DATABASE your_db_name;
    ```

3. Create a `.env` file in the root of the project with the following environment variables for connecting to the PostgreSQL database:

    ```env
    PGDIALECT=your_host
    PGUSER=your_db_password
    PGPASSWD=your_db_user
    PGHOST=your_host_adress
    PGPORT=5432
    PGDB=your_db_name
    WORK_DIR=your_working_directory
    ```

4. Set up and activate your virtual environment:

    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

5. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

You are now ready to start working on this workshop.


# Creating a Dashboard in Power BI from PostgreSQL

Follow these steps to connect Power BI to a PostgreSQL database and create your dashboard.

## Step 1: Obtain Data

Ensure you have the dataset and that it is already loaded into a PostgreSQL database.

## Step 2: Open Power BI Desktop

1. **Launch Power BI Desktop:** Open Power BI Desktop on your computer.

## Step 3: Connect to PostgreSQL

1. **Go to Home Tab:**
   - Click on the **"Home"** tab in the top menu.

2. **Get Data:**
   - Click on the **"Get Data"** button on the Home ribbon.

3. **Select Data Source:**
   - In the "Get Data" window, select **"More…"** to open the full list of data sources.
   - Scroll down and choose **"PostgreSQL database"** from the list.
   - Click **"Connect"**.
     


4. **Enter Server Details:**
   - In the **"PostgreSQL database"** window, enter the **Server** and **Database** details:
     - **Server:** Your PostgreSQL server address (e.g., `localhost` or `your_host`).
     - **Database:** The name of your PostgreSQL database.


5. **Verify Connection:**
   - Power BI will attempt to connect to your PostgreSQL database. If successful, you will see a list of available tables.

## Step 5: Select Tables

1. **Select the Desired Tables:**

2. **Preview and Transform Data (Optional):**
   - If you need to make any transformations or adjustments to the data before loading it into Power BI, click **"Transform Data"** instead of **"Load"**. This will open the Power Query Editor where you can perform data cleaning and transformation tasks.

## Step 6: Build Your Dashboard

   - Once your data is loaded into Power BI, you can start creating visualizations. Drag and drop fields from your tables onto the report canvas to create charts, tables, and other visual elements.
   - Customize the layout and design of your dashboard. Add filters, slicers, and interactive elements to make your dashboard informative and user-friendly.
   - Save your Power BI file and, if desired, publish it to the Power BI service for sharing and collaboration.

Congratulations! You have successfully created a dashboard in Power BI using data from a PostgreSQL database. 