# Usa la imagen de Airflow específica
FROM apache/airflow:2.5.1-python3.10

# Cambia al usuario root para instalar dependencias del sistema
USER root

# Instala git y librerías necesarias para PostgreSQL
RUN apt-get update && apt-get install -y git libpq-dev && apt-get clean

# Cambia de nuevo al usuario airflow para instalar las dependencias de Python
USER airflow

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /requirements.txt

# Instala los paquetes de Python como el usuario airflow
RUN pip install --no-cache-dir -r /requirements.txt
