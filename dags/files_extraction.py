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
import tempfile
import boto3

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
    def downloading_from_s3():
            # s3_client = boto3.client('s3')
            s3_hook = S3Hook(aws_conn_id="minin_s3")
            s3_key="orders/tolldata.tgz"
            bucket_name="vehicle"
            
            # s3_key="orders.csv"
            # bucket_name="airflow"
            local_path = os.path.dirname(__file__)
            # local_path= os.path.join(local_path, 'file.tgz')
            # aws_conn_id="minin_s3"
            # local_file_path = os.path.join(dag_folder_path, 'file.txt')
            # local_path="C:/Users/avula/Downloads/airflow-setup/dags/"

            try:
                # Download the file from S3 to the local file path
                s3_hook.download_file(bucket_name=bucket_name, key=s3_key, local_path=local_path)
                print(f"File downloaded successfully to {local_path}")
            except Exception as e:
                print(f"Error downloading file: {e}")
            return local_path
    
    def change_extension_to_tgz():
        local_path = os.path.dirname(__file__)
    # List all files in the directory
        for filename in os.listdir(local_path):
            # Check if the filename starts with "airflow_tmp"
            if filename.startswith("airflow_tmp"):
                # Construct the current and new file paths
                current_file_path = os.path.join(local_path, filename)
                new_file_path = os.path.join(local_path, filename + ".tgz")

                # Rename the file to change its extension to ".tgz"
                os.rename(current_file_path, new_file_path)

                print(f"Changed extension of {filename} to .tgz")
    

    def extract_files():
        directory=os.path.dirname(__file__)
        try:
            # List all files in the directory
            files = os.listdir(directory)
            
            # Filter the .tgz file from the list
            tgz_files = [file for file in files if file.endswith(".tgz")]

            if len(tgz_files) == 0:
                print("Error: No .tgz file found in the directory.")
                return
            
            # Assuming only one .tgz file is present, extract the first one found
            tgz_file_path = os.path.join(directory, tgz_files[0])

            # Open the .tgz file for reading
            with tarfile.open(tgz_file_path, 'r:gz') as tar:
                print("Extracting files...")
                # Extract all the contents into the specified directory
                tar.extractall(directory)
            print("Extraction complete.")
        except FileNotFoundError:
            print(f"Error: Directory {directory} not found.")
        except tarfile.ReadError:
            print(f"Error: Unable to open or read the file {tgz_file_path}.")
        except tarfile.CompressionError:
            print(f"Error: Unable to decompress the file {tgz_file_path}.")
        except tarfile.TarError:
            print(f"Error: An error occurred while extracting the file {tgz_file_path}.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")

    def delete_files_with_dot_prefix():
        directory=os.path.dirname(__file__)
        
        # Get a list of all files in the directory
        files = os.listdir(directory)
        
        # Iterate through the files
        for file in files:
            # Check if the file name starts with a dot (.)
            if file.startswith('.'):
                # Construct the full path to the file
                file_path = os.path.join(directory, file)
                
                # Delete the file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")


        
    # task1=PythonOperator(
    #     task_id="upload_to_s3",
    #     python_callable=upload_to_s3
    # )
    # task2=PythonOperator(
    #     task_id="downloading_from_s3",
    #     python_callable=downloading_from_s3
    # )
    # task3=PythonOperator(
    #     task_id="change_extension_to_tgz",
    #     python_callable=change_extension_to_tgz
    # )
    task4=PythonOperator(
        task_id="delete_files_with_dot_prefix",
        python_callable=delete_files_with_dot_prefix
    )
    # task1>>task2
    # task2>>task3
