"""API: http://172.17.0.2:9000  http://127.0.0.1:9000
WebUI: http://172.17.0.2:9001 http://127.0.0.1:9001
"MINIO_ROOT_USER=ROOTUSER" `
"MINIO_ROOT_PASSWORD=CHANGEME123" `
"""
#apache-airflow-providers-amazon          8.19.0
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5)
}
with DAG(
    default_args=default_args,
    dag_id="miniouss3dag",
    start_date=datetime(2024, 3, 31, 2),
    schedule_interval="5 4 * * *",
    description="This is my first DAG building with Python Operator"
) as dag:
    task1=S3KeySensor(
        task_id="s1minio_sensor",
        bucket_name="airflow",
        bucket_key="data.csv",
        aws_conn_id="minin_s3", # same as connection id in airflow
        mode="poke",
        timeout=30,
        poke_interval=5,



    )