from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
import csv
import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import os
import tarfile
import pandas as pd
import csv
import time
import shutil

default_args={
    "owner":"airflow",
    "retries":3,
    "retry_delay": timedelta(minutes=5)
    
}
with DAG(
    dag_id="files_ext",
    default_args=default_args,
    start_date=datetime(2024,3,31,2),
    schedule_interval="@daily",
    description="this is my first dag building with python operator"



) as dag:
    def upload_to_s3():
        s3_hook=S3Hook(aws_conn_id="minin_s3")
        s3_hook.load_file(
            filename="dags/tolldata.tgz",
            key="orders/tolldata.tgz",
            bucket_name="vehicle",
            replace=True
    )
    def extract_zip_and_upload_to_s3():
    # Upload zip file to S3
        local_to_s3 = LocalFilesystemToS3Operator(
            task_id='local_to_s3',
            src="../data/tolldata/toll_data.zip",
            dest="vehicle",
            aws_conn_id="minin_s3",
            overwrite=True
    )

    # Extract zip file in S3
        s3_unzip = S3UnzipOperator(
            task_id='s3_unzip',
            source_s3_key="vehicle/zipfile.zip",
            dest_s3_bucket="vehicle",
            dest_s3_key="extracted/",
            overwrite=True
        )

        local_to_s3 >> s3_unzip
    task1=PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3
    )