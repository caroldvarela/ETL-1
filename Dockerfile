# Use the specific Airflow image
FROM apache/airflow:2.5.1-python3.10

# Switch to the root user to install system dependencies
USER root

# Install Git and necessary libraries for PostgreSQL
RUN apt-get update && apt-get install -y git libpq-dev && apt-get clean

# Switch back to the airflow user to install the Python dependencies
USER airflow

# Copy the requirements.txt file to the container
COPY requirements.txt /requirements.txt

# Install the Python packages as the airflow user
RUN pip install --no-cache-dir -r /requirements.txt