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

2.  Create a Virtual Environment:  

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    
3. Install the Required Dependencies:

    ```env
    pip install -r requirements.txt
    ```

## PostgresSQL

- **Set Up PostgreSQL**  
   Install and configure PostgreSQL:
   ```bash
   sudo apt update
   sudo apt-get -y install postgresql postgresql-contrib
   sudo service postgresql start
   sudo apt-get install libpq-dev python3-dev

- **Log in to PostgreSQL**  
   Run the following commands to log in:
   ```bash
   sudo -i -u postgres
   psql

- **Create a New Database and User**  
   Run the following SQL commands to create a new user and database:
   ```sql
   CREATE USER <your_user> WITH PASSWORD '<your_password>';
   ALTER USER <your_user> WITH SUPERUSER;
   CREATE DATABASE workshop2 OWNER <your_user>;
   
- **Configure PostgreSQL for External Access (Optional for PowerBI)**  
   The PostgreSQL configuration files are generally located in `/etc/postgresql/{version}/main/`
   Edit the `postgresql.conf` file to allow external connections
   
   ```bash
   listen_addresses = '*'
   ssl = off
   
-  **Edit the pg_hba.conf File**  
   Allow connections from your local IP by adding the following line:
   ```plaintext
   host    all             all             <your-ip>/32         md5

- **Set Up pgAdmin 4 (Optional)**  
   To install pgAdmin 4, run the following commands:
   ```bash
   sudo apt install curl
   sudo curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
   sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
   sudo apt install pgadmin4

## Configuration of the .env File

- **Create a .env File**  
   Create a `.env` file with the following configuration:
   ```plaintext
   PGDIALECT=postgresql
   PGUSER=<your_user>
   PGPASSWD=<your_password>
   PGHOST=localhost
   PGPORT=5432
   PGDB=workshop2
   WORK_DIR=<your_working_directory>

## Airflow

 - **Create the Airflow Directory:**  
   ```bash
   mkdir airflow
   ```

 - **Set the Airflow Home Environment Variable:**  
   ```bash
   export AIRFLOW_HOME=~/airflow
   ```

 - **Configure the airflow.cfg File**  
   The `airflow.cfg` file is located in the directory specified by `AIRFLOW_HOME`. To modify the `dags_folder`, set it to the path of your `dag.py` file:
   ```ini
   dags_folder = /path/to/your/dag
   ```

 - **Initialize the Airflow Database:**  
   ```bash
   airflow db init
   ```

 - **Start Airflow:**  
   ```bash
   airflow standalone
   ```
   
 - **Run the Airflow DAG**   
   Navigate to the **Airflow UI**, enable the DAG, and trigger it manually.
   
You can now access the Airflow UI using the generated **credentials**.


You are now ready to start working on this workshop.


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
