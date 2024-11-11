# ETL Project 

Presented by 
- Jhonatan Steven Morales Hernandez: jhonatan.morales@uao.edu.co
- Carol Dayana Varela Cortez: carol.varela@uao.edu.co
- Manuel Alejandro Gruezo manuel.gruezo@uao.edu.co

## 📝 Introduction

Exploratory Data Analysis (EDA) is a crucial step in any data science project, as it allows us to better understand the structure, relationships, and patterns within the data before conducting any advanced modeling or analysis.

In this project, we will work with two main datasets:

1. **💓 Cardio Train Dataset**: This dataset contains information on various health indicators of individuals, such as age, gender, height, weight, blood pressure, cholesterol levels, and more. The goal is to explore these data points to identify potential correlations and patterns that could be useful in predicting cardiovascular diseases.
   
2. **⚠️ Cause Of Deaths**: This dataset provides information on causes of death at a global level, broken down by country and year. It records a wide range of diseases and conditions, such as meningitis, respiratory diseases, and various forms of cancer, among others. However, the main focus is on mortality associated with cardiovascular diseases.

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

This project is developed within a virtual machine running **Ubuntu**. The dashboard has been created using Power BI on a Windows machine.

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
- **Docker** <img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/docker-icon.png" alt="Docker" width="50px" height="21px">

### Repository Organization

- **dags:** This folder includes DAG files necessary for orchestrating ETL workflows in Apache Airflow. It contains `__init__.py`, `dags.py`, and `etl.py`, which are essential for defining tasks and scheduling.

- **data:** This folder holds the raw data files used in the project, including `cardio_train.csv`, `cause_of_deaths.csv`, and `owid.csv`. These files serve as the input data for analysis and model training.

- **logs:** A folder containing log files that help in monitoring the workflow processes and identifying issues during execution. The `.gitkeep` file ensures that the folder is tracked by Git even when empty.

- **notebooks:** This directory contains Jupyter notebooks used for exploratory data analysis (EDA) and other key processes:
  - **EDA/002_EDA_dataset.ipynb** – Initial EDA for understanding the dataset.
  - **005_EDA_API.ipynb** – EDA related to API data sources.
  - **Great Expectations (GX)/006_great_expectations.ipynb** – Notebook for data validation using Great Expectations.
  - **004_API.ipynb** – Notebook for merging data obtained from the API.
  - **database_process/001_DataSetup.ipynb** – Notebook for setting up the database.
  - **003_database_processed.ipynb** – Notebook documenting the data processing stage.

- **gx:** This folder is dedicated to Great Expectations for data validation. It contains:
  - **expectations** – JSON files like `cardio_train_expectations.json`, `cause_of_deaths_expectations.json`, and `owid_expectations.json` define the validation rules.
  - **plugins/custom_data_docs/styles/data_docs_custom_styles.css** – Custom styles for the data documentation.
  - **.ge_store_backend_id** and **great_expectations.yml** – Configuration files for managing expectations and storing metadata.

- **src:** Contains core code for database interaction, models, and data validation:
  - **database** – Code for database connection and table creation, including `dbconnection.py` and `createTable.py`.
  - **gx_utils** – Contains `validation.py` for running data validations.
  - **model** – Holds `models.py` and related files defining the data model structure.
  - **streaming** – Code for data streaming operations, including `data_to_powerbi.py` and `kafka_utils.py`.
  - **transform** – Code for data transformation, with scripts like `DimensionalModels.py` and `TransformData.py`.

- **Dashboard-streaming.mp4 / Dashboard.pdf:** Visual materials showcasing the dashboard and how data is presented using streaming updates.

- **Dockerfile / Dockerfile.jupyter:** Docker configuration files for setting up the environment, including Jupyter for development.

- **Documentation.pdf:** Comprehensive documentation for the project, outlining methodologies and results.

- **example_env:** A template environment file to guide users in setting up their environment variables.

- **main.py:** The main script that acts as an entry point for the project.

- **requirements.txt:** Lists all the dependencies needed to run the project.

- **docker-compose.yml:** Configuration file for orchestrating multi-container Docker applications.


### Requirements
1. Install Python : [Python Downloads](https://www.python.org/downloads/)
2. Install Power BI : [Install Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494) 

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

2.  Create a Virtual Environment:  

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    
3. Install the Required Dependencies:

    ```env
    pip install -r requirements.txt
    ```

## Configuration of the .env File

- **Create a .env File**  
   Create a `.env` file with the following configuration:
   ```plaintext
   # Airflow Configuration
   AIRFLOW_UID=50000
   AIRFLOW_GID=50000

   # PostgreSQL Configuration
   PGUSER=airflow
   PGPASSWD=airflow
   PGDIALECT=postgresql
   PGHOST=postgres
   PGPORT=5432
   PGDB=airflow

   # Kafka Configuration
   KAFKA_BROKER=kafka:9092

   # Airflow Admin User
   AIRFLOW_ADMIN_USER=admin
   AIRFLOW_ADMIN_PASSWORD=admin
   AIRFLOW_ADMIN_EMAIL=admin@example.com

   # Power BI API URL (for data streaming)
   POWERBI_API=<your_power_bi_api_url>

   # Working Directory for Airflow
   WORK_DIR=/opt/airflow

# Steps to Run the Project

1. **Start the Containers**
   Run the following command to create and start the necessary Docker containers:
   ```bash
   docker-compose up -d
   ```
## Access Jupyter Notebook

1. Open your web browser and navigate to [http://localhost:8888](http://localhost:8888).
2. Locate and open the notebook `003_database_processed.ipynb` located in the `database_process` folder.
3. Run all the cells in the notebook to process the data and prepare the database.

## Start Listening for Data Streaming

1. Open a new terminal or command prompt window.
2. Ensure that the streaming process is actively listening by running any necessary commands or scripts as specified in your project documentation.

## Monitor Airflow

1. Once the Jupyter Notebook is executed and the containers are running, navigate to [http://localhost:8080](http://localhost:8080) to access the Airflow web interface.
2. Verify that the DAGs are running as expected and monitor the data processing workflow.

## Completion and Observation

1. Wait for Airflow to complete the data processing tasks. You can monitor the progress and logs directly in the Airflow interface.
2. Once completed, you can proceed to validate the outputs or perform further analysis as needed.



# Connect Power BI to PostgreSQL

Do you want to create your own dashboard? You’ll probably need to do this:

## Steps to Configure the Bridged Adapter

1. **Open VirtualBox:**
   - Start VirtualBox on your computer.

2. **Select the Virtual Machine:**
   - From the list of virtual machines, select the one you want to configure.

3. **Open Settings:**
   - Click the "Settings" button (the gear icon) at the top.

4. **Go to the Network Tab:**
   - In the settings window, select the "Network" tab.

5. **Enable the Adapter:**
   - Check the box "Enable Network Adapter."

6. **Select the Adapter Type:**
   - In the "Attached to" field, select "Bridged Adapter."



## Open Power BI

7. **Start Power BI Desktop** on your Windows machine.

8. **Get Data:**
   - On the home screen, click "Get Data."
     
   ![image](https://github.com/caroldvarela/images/blob/main/Dashboard_1.png)
9. **Select PostgreSQL:**
   - In the "Get Data" window, choose "PostgreSQL Database" and click "Connect."

   ![image](https://github.com/caroldvarela/images/blob/main/Dashboard_2.png)
10. **Configure the Connection:**
    - In the connection dialog, enter the following information:
      - **Server:** `server_ip:port` (by default, `localhost:5432` if connecting to your local machine).
      - **Database:** The name of the database you want to connect to.
   ![image](https://github.com/caroldvarela/images/blob/main/workshop2-1.png)

11. **Authentication:**
    - Select the authentication method "Database" and enter your PostgreSQL username and password.
   ![image](https://github.com/caroldvarela/images/blob/main/workshop2-2.png)
12. **Load Data:**
    - Click "Connect" and if the connection is successful, you will see the available tables in your database. Select the tables you want to import and click "Load."
   - Once your data is loaded into Power BI, you can start creating visualizations. Drag and drop fields from your tables onto the report canvas to create charts, tables, and other visual elements.
   - Customize the layout and design of your dashboard. Add filters, slicers, and interactive elements to make your dashboard informative and user-friendly.
   - Save your Power BI file and, if desired, publish it to the Power BI service for sharing and collaboration.


Congratulations! You have successfully created a dashboard in Power BI using data from a PostgreSQL database. 
