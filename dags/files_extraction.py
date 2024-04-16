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
    def exst():
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
    
    
    def ext():
        # Create a temporary directory within the DAG folder
        DAG_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
        with tempfile.TemporaryDirectory(dir=DAG_FOLDER_PATH) as temp_dir:
            print("Temporary directory created:", temp_dir)

            # Download the zip file from S3
            s3_hook = S3Hook(aws_conn_id="minin_s3")
            local_zip_path = os.path.join(temp_dir, 'tolldata.tgz')  # Full file path including filename
            print("Downloading file...")
            s3_hook.download_file(key="orders/tolldata.tgz", bucket_name="vehicle", local_path=local_zip_path)

        return local_zip_path  # Return the path where the file was downloaded

    def extract_and_upload_to_s3():
    # Create a temporary directory within the DAG folder
        DAG_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
        with tempfile.TemporaryDirectory(dir=DAG_FOLDER_PATH) as temp_dir:
            print("Temporary directory created:", temp_dir)

            # Download the zip file from S3
            s3_hook = S3Hook(aws_conn_id="minin_s3")
            # local_zip_path = os.path.join(temp_dir, 'tolldata.tgz')
            print("Downloading file...")
            local_zip_path="/Users/avula/Downloads/airflow-setup/data/"
            s3_hook.download_file(key="orders/tolldata.tgz", bucket_name="vehicle", local_path=local_zip_path)
            print("File downloaded:", local_zip_path)

            try:
                # Open the tgz file for reading
                with tarfile.open(local_zip_path, 'r:gz') as tar:
                    print("Extracting files...")
                    # Extract all the contents into the specified directory
                    tar.extractall(temp_dir)
                print("Extraction complete.")

                # Upload the extracted files to S3
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    s3_hook.load_file(filename=file_path, key=f"extracted_files/{filename}", bucket_name="vehicle", replace=True)

            except FileNotFoundError:
                print(f"Error: File {local_zip_path} not found.")
            except tarfile.ReadError:
                print(f"Error: Unable to open or read the file {local_zip_path}.")
            except tarfile.CompressionError:
                print(f"Error: Unable to decompress the file {local_zip_path}.")
            except tarfile.TarError:
                print(f"Error: An error occurred while extracting the file {local_zip_path}.")
            except Exception as e:
                print(f"Error: An unexpected error occurred: {e}")


            # Perform operations within the temporary directory
            # For example, create files, download files, extract files, etc.

            # Example: create a temporary file within the temporary directory
            # temp_file_path = os.path.join(newwww, 'temp_file2.txt')
            # with open(temp_file_path, 'w') as temp_file:
            #     temp_file.write('Hello, temporary world!')
            # #locate file in the temporary directory
            # print("Temporary file created:", temp_file_path)
        return newwww

    def extract_files():
        s3_hook = S3Hook(aws_conn_id="minin_s3")
        # local_path="dags/"
        local_path = "dags/tolldata.tgz"  # Temporary path to download the file
        extract_path = "dags/extracted_files"
        print(local_path)
        s3_hook.download_file(key="orders/tolldata.tgz", bucket_name="vehicle", local_path=local_path)
        try:
        # Open the tgz file for reading
            with tarfile.open(local_path, 'r:gz') as tar:
                print("Extracting files...")
                # Extract all the contents into the specified directory
                # tar.extractall("dags/")
                tar.extractall(extract_path)
            print("Extraction complete.")
            for filename in os.listdir("dags/"):
                file_path = os.path.join("dags/", filename)
                s3_hook.load_file(filename=file_path, key=f"extracted_files/{filename}", bucket_name="vehicle", replace=True)
            # Clean up: delete the temporary directory and downloaded tgz file
            os.remove(local_path)
            # os.rmdir("local_path")
        except FileNotFoundError:
            print(f"Error: File {local_path} not found.")
        except tarfile.ReadError:
            print(f"Error: Unable to open or read the file {local_path}.")
        except tarfile.CompressionError:
            print(f"Error: Unable to decompress the file {local_path}.")
        except tarfile.TarError:
            print(f"Error: An error occurred while extracting the file {local_path}.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")


        
    # task1=PythonOperator(
    #     task_id="upload_to_s3",
    #     python_callable=upload_to_s3
    # )
    task2=PythonOperator(
        task_id="exst",
        python_callable=exst
    )
    # task1>>task2