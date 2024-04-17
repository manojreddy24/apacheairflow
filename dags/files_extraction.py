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

    def create_directory():
        # directory=os.path.dirname(__file__)
        # files = os.listdir(directory)
        # print(f"Files in the directory: {files}")
        current_script_directory = os.path.dirname(os.path.abspath(__file__))

        # Append the relative path to the parent directory
        parent_directory = os.path.join(current_script_directory, "..")
        #creat directory directory
        new_directory = os.path.join(parent_directory, "data")
        
        try:
            os.mkdir(new_directory)
            print("Directory created successfully.")
        except FileExistsError:
            print("Directory already exists.")

        

        # Use the parent directory for listing files
        files = os.listdir(parent_directory)
        return files
    

    def extract_files():
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        new_directory = os.path.join(parent_directory, "data")
        filesnew = os.listdir(new_directory)
        try:
            # List all files in the directory
            files = os.listdir(current_script_directory)
            
            # Filter the .tgz file from the list
            tgz_files = [file for file in files if file.endswith(".tgz")]

            if len(tgz_files) == 0:
                print("Error: No .tgz file found in the directory.")
                return
            
            # Assuming only one .tgz file is present, extract the first one found
            tgz_file_path = os.path.join(current_script_directory, tgz_files[0])

            # Open the .tgz file for reading
            with tarfile.open(tgz_file_path, 'r:gz') as tar:
                print("Extracting files...")
                # Extract all the contents into the specified directory
                tar.extractall(new_directory)
            print("Extraction complete.")
        except FileNotFoundError:
            print(f"Error: Directory {new_directory} not found.")
        except tarfile.ReadError:
            print(f"Error: Unable to open or read the file {tgz_file_path}.")
        except tarfile.CompressionError:
            print(f"Error: Unable to decompress the file {tgz_file_path}.")
        except tarfile.TarError:
            print(f"Error: An error occurred while extracting the file {tgz_file_path}.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
        allfiles = os.listdir(new_directory)
        return allfiles

    def delete_files_with_dot_prefix():
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        new_directory = os.path.join(parent_directory, "data")
        # filesnew = os.listdir(new_directory)
        
        # Get a list of all files in the directory
        files = os.listdir(new_directory)
        print(f"Files in the directory: {files}")
        filename="fileformats.txt"
        file_paths = os.path.join(new_directory, filename)
        try:
            os.remove(file_paths)
            print(f"File '{filename}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except PermissionError:
            print(f"No permission to delete file '{filename}'.")
        except Exception as e:
            print(f"An error occurred while deleting file '{filename}': {e}")
        
        # Iterate through the files
        for file in files:
            # Check if the file name starts with a dot (.)
            if file.startswith('.'):
                # Construct the full path to the file
                file_path = os.path.join(new_directory, file)
                
                # Delete the file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        new_files = os.listdir(new_directory)

        return new_files
    def extract_data_from_csv():
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        full_folder_path = os.path.join(parent_directory, "data")
        extraction_done_folder=os.path.join(parent_directory, "extraction_done")
        final_path=os.path.join(parent_directory, "destination")

        
        files = os.listdir(full_folder_path)
        # Initialize an empty list to store the modified data
        modified_data = []
       
        # full_folder_path = os.path.join(cwd, folder_path)

        # Check if the folder exists
        if os.path.exists(full_folder_path) and os.path.isdir(full_folder_path):
            # Create the extraction_done folder if it doesn't exist
            # extraction_done_folder = os.path.join(cwd, "../extraction_done")
            print(extraction_done_folder)
            # final_path = os.path.join(cwd, "../destination")
            try:
                os.mkdir(extraction_done_folder)
                os.mkdir(final_path)
                print("Directory created successfully.")
            except FileExistsError:
                print("Directory already exists.")
             


          
            
            # Initialize a counter to keep track of the number of CSV files
            csv_count = 0
            
            # Iterate over the files
            for file in files:
                # Check if the file is a CSV file
                if file.endswith(".csv"):
                    # Increment the CSV file counter
                    csv_count += 1
                    
                    # Construct the full path to the CSV file
                    file_path = os.path.join(full_folder_path, file)

                    # Read the contents of the CSV file
                    with open(file_path, 'r') as f:
                        # Skip the header line
                        # next(f)
                        # Read the remaining lines
                        reader = csv.reader(f)
                        for row in reader:
                            # Insert rows for Rowid, Timestamp, Anonymized Vehicle number, and Vehicle type
                            modified_row = [
                                csv_count,  # Rowid (using csv_count as an example)
                            # Timestamp
                                row[1],  # Anonymized Vehicle number (assuming it's the first column)
                                row[2],  # Vehicle type (assuming it's the second column)
                                row[3],
                            ]
                            # Append the modified row to the list
                            modified_data.append(modified_row)

                    # Move the source CSV file to the extraction_done folder
                    try:
                        # Check if the destination file already exists
                        if os.path.exists(extraction_done_folder):
                            os.remove(extraction_done_folder)  # Remove the existing file
                            print(f"Existing file '{extraction_done_folder}' removed.")

                        # Move the source file to the destination
                        shutil.move(file_path, extraction_done_folder)
                        print(f"File '{file_path}' moved to '{extraction_done_folder}' successfully.")
                    except FileNotFoundError:
                        print(f"Source file '{file_path}' not found.")
                    except PermissionError:
                        print(f"No permission to move file '{file_path}'.")
                    except Exception as e:
                        print(f"An error occurred while moving file '{file_path}': {e}")
                    
                    # shutil.move(file_path, extraction_done_folder)
                    # print(f"Moved {file} to extraction_done folder.")

            # Print the total number of CSV files found
            print("Total CSV files found:", csv_count)
            
            # Check if any CSV files were found
            if modified_data:
                # Define the path for the new CSV file
                new_csv_file_path = os.path.join(final_path,"csv_data.csv")  # Adjust the path as needed
                
                # Write the modified data to a new CSV file
                with open(new_csv_file_path, 'w', newline='') as new_csv_file:
                    writer = csv.writer(new_csv_file)
                    # Write header
                    writer.writerow(["Rowid", "Timestamp", "Anonymized Vehicle number", "Vehicle type"])
                    # Write data
                    writer.writerows(modified_data)
                
                print(f"New CSV file created: {new_csv_file_path}")
            else:
                print("No CSV files found in the folder.")
        else:
            print(f"Folder {full_folder_path} does not exist.")
        final_path_files=os.listdir(final_path)

        return final_path_files
    

    def extract_data_from_tsv():
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        full_folder_path = os.path.join(parent_directory, "data")
        extraction_done_folder=os.path.join(parent_directory, "extraction_done")
        final_path=os.path.join(parent_directory, "destination")

        
        files = os.listdir(full_folder_path)
    # Initialize an empty list to store the modified data
        modified_data = []

        # Check if the folder exists
        if os.path.exists(full_folder_path) and os.path.isdir(full_folder_path):
            # Create the extraction_done folder if it doesn't exist
            try:
                os.mkdir(extraction_done_folder)
                os.mkdir(final_path)
                print("Directory created successfully.")
            except FileExistsError:
                print("Directory already exists.")
            
            
            # Initialize a counter to keep track of the number of tSV files
            tsv_count = 0
            
            # Iterate over the files
            for file in files:
                # Check if the file is a tSV file
                if file.endswith(".tsv"):
                    # Increment the CSV file counter
                    tsv_count += 1
                    
                    # Construct the full path to the tSV file
                    file_path = os.path.join(full_folder_path, file)

                    # Read the contents of the tSV file
                    with open(file_path, 'r') as f:
                        # Skip the header line
                        # next(f)
                        # Read the remaining lines
                        reader = csv.reader(f,delimiter='\t')
                        for row in reader:
                            # Insert rows for Rowid, Timestamp, Anonymized Vehicle number, and Vehicle type
                            extracted_row = [row[4], row[5], row[6]]
                            # Append the modified row to the list
                            modified_data.append(extracted_row)

                    # Move the source tSV file to the extraction_done folder
                    
                    try:
                        # Check if the destination file already exists
                        if os.path.exists(extraction_done_folder):
                            os.remove(extraction_done_folder)  # Remove the existing file
                            print(f"Existing file '{extraction_done_folder}' removed.")

                        # Move the source file to the destination
                        shutil.move(file_path, extraction_done_folder)
                        print(f"File '{file_path}' moved to '{extraction_done_folder}' successfully.")
                    except FileNotFoundError:
                        print(f"Source file '{file_path}' not found.")
                    except PermissionError:
                        print(f"No permission to move file '{file_path}'.")
                    except Exception as e:
                        print(f"An error occurred while moving file '{file_path}': {e}")

            # Print the total number of tSV files found
            print("Total tSV files found:", tsv_count)
            
            # Check if any tSV files were found
            if modified_data:
                # Define the path for the new CSV file
                new_tsv_file_path = os.path.join(final_path,"tsv_data.csv")  # Adjust the path as needed
                
                # Write the modified data to a new tSV file
                with open(new_tsv_file_path, 'w', newline='') as new_csv_file:
                    writer = csv.writer(new_csv_file)
                    # Write header
                    writer.writerow(["Number of axles", "Tollplaza id", "Tollplaza code"])
                    # Write data
                    writer.writerows(modified_data)
                
                print(f"New tSV file created: {new_tsv_file_path}")
            else:
                print("No tSV files found in the folder.")
        else:
            print(f"Folder {full_folder_path} does not exist.")
        final_path_files=os.listdir(final_path)

        return final_path_files
    
    def extract_data_from_fixed_width():
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        full_folder_path = os.path.join(parent_directory, "data")
        extraction_done_folder=os.path.join(parent_directory, "extraction_done")
        final_path=os.path.join(parent_directory, "destination")

        
        files = os.listdir(full_folder_path)
        # Initialize an empty list to store the modified data
        modified_data = []

        # Check if the folder exists
        if os.path.exists(full_folder_path) and os.path.isdir(full_folder_path):
            # Create the extraction_done folder if it doesn't exist
            
            os.makedirs(extraction_done_folder, exist_ok=True)

            # List all files in the folder
            
            
            # Initialize a counter to keep track of the number of txt files
            txt_count = 0
            colspecs = [(0, 6), (6, 32), (33, 43), (43, 48), (49, 60), (57, 61), (61, 70)]

        # Define column names
            column_names = ["Column1", "Column2", "Column3", "Column4", "Column5", "Type of Payment code", "Vehicle Code"]
            
            # Iterate over the files
            for file in files:
                # Check if the file is a txt file
                if file.endswith(".txt"):
                    # Increment the CSV file counter
                    txt_count += 1
                    
                    # Construct the full path to the txt file
                    file_path = os.path.join(full_folder_path, file)

                    # Read the contents of the txt file
                    with open(file_path, 'r') as f:
                        # Skip the header line
                        # next(f)
                        df = pd.read_fwf(f, colspecs=colspecs, header=None, names=column_names)
                        extracted_df = df[["Type of Payment code", "Vehicle Code"]]
                        # Write the renamed data to a CSV file
                        extracted_df.to_csv(final_path+"/txt_data.csv", index=False)

                    # Move the source txt file to the extraction_done folder
                    
                    try:
                        # Check if the destination file already exists
                        if os.path.exists(extraction_done_folder):
                            os.remove(extraction_done_folder)  # Remove the existing file
                            print(f"Existing file '{extraction_done_folder}' removed.")

                        # Move the source file to the destination
                        shutil.move(file_path, extraction_done_folder)
                        print(f"File '{file_path}' moved to '{extraction_done_folder}' successfully.")
                    except FileNotFoundError:
                        print(f"Source file '{file_path}' not found.")
                    except PermissionError:
                        print(f"No permission to move file '{file_path}'.")
                    except Exception as e:
                        print(f"An error occurred while moving file '{file_path}': {e}")
                    

            # Print the total number of txt files found
            print("Total txt files found:", txt_count)
            
            # Check if any txt files were found
            if modified_data:
                # Define the path for the new txt file
                new_txt_file_path = os.path.join(final_path,"txt_data.csv")  # Adjust the path as needed
                
                # Write the modified data to a new txt file
                with open(new_txt_file_path, 'w', newline='') as new_csv_file:
                    writer = csv.writer(new_csv_file)
                    # Write header
                    writer.writerow(["Number of axles", "Tollplaza id", "Tollplaza code"])
                    # Write data
                    writer.writerows(modified_data)
                
                print(f"New txt file created: {new_txt_file_path}")
            else:
                print("No txt files found in the folder.")
        else:
            print(f"Folder {full_folder_path} does not exist.")
        final_path_files=os.listdir(final_path)

        return final_path_files
    def merge_csv_files():
        # Specify the paths to the CSV files
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        full_folder_path = os.path.join(parent_directory, "data")
        extraction_done_folder=os.path.join(parent_directory, "extraction_done")
        final_path=os.path.join(parent_directory, "destination")

        
        # files = os.listdir(final_path)
        print("files",final_path)
        csv_file1 = os.path.join(final_path, 'csv_data.csv')
        # print(csv_file1)
        csv_file2 = os.path.join(final_path, 'tsv_data.csv')
        csv_file3 = os.path.join(final_path, 'txt_data.csv')
    
        # Read each CSV file into a pandas DataFrame
        df1 = pd.read_csv(csv_file1)
        df2 = pd.read_csv(csv_file2)
        df3 = pd.read_csv(csv_file3)
    # Concatenate the columns from each file
        merged_df = pd.concat([df1, df2, df3], axis=1)
        
        # Merge the DataFrames based on common columns
    
        
        
        # Merge the DataFrames
        # merged_df = pd.concat([df1, df2, df3], ignore_index=True)
        
        # Write the merged DataFrame to a new CSV file
        output_file_path = os.path.join(final_path, "merged.csv")
        merged_df.to_csv(output_file_path, index=False)
        print("pdf merged successfully to {output_file_path}")
        final_path_files=os.listdir(final_path)

        return final_path_files
    def transform_data():
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        full_folder_path = os.path.join(parent_directory, "data")
        extraction_done_folder=os.path.join(parent_directory, "extraction_done")
        final_path=os.path.join(parent_directory, "destination")

        
        file_path = os.path.join(final_path, "merged.csv")

        # input_file = "../destination/merged.csv"
        df = pd.read_csv(file_path)
        # Perform data transformation here
        df['Vehicle type'] = df['Vehicle type'].str.upper()
        output_file_path = os.path.join(final_path, 'transformed_data.csv')
        df.to_csv(output_file_path, index=False)  
        final_path_files=os.listdir(final_path)

        return final_path_files
    def uploadmergedfile_to_s3():
        current_script_directory=os.path.dirname(__file__)
        parent_directory = os.path.join(current_script_directory, "..")
        full_folder_path = os.path.join(parent_directory, "data")
        extraction_done_folder=os.path.join(parent_directory, "extraction_done")
        final_path=os.path.join(parent_directory, "destination")

        
        file_path = os.path.join(final_path, "transformed_data.csv")
        s3_hook=S3Hook(aws_conn_id="minin_s3")
        s3_hook.load_file(
            filename=file_path,
            key="orders/transformed_data.csv",
            bucket_name="vehicle",
            replace=True
    )




        
    # task1=PythonOperator(
    #     task_id="upload_to_s3",
    #     python_callable=upload_to_s3
    # )
    task2=PythonOperator(
        task_id="downloading_from_s3",
        python_callable=downloading_from_s3
    )
    task3=PythonOperator(
        task_id="change_extension_to_tgz",
        python_callable=change_extension_to_tgz
    )
  
    task4=PythonOperator(
        task_id="create_directory",
        python_callable=create_directory
    )
    task5=PythonOperator(
        task_id="extract_files",
        python_callable=extract_files
    )
    task6=PythonOperator(
        task_id="delete_files_with_dot_prefix",
        python_callable=delete_files_with_dot_prefix
    )
    task7=PythonOperator(
        task_id="extract_data_from_csv",
        python_callable=extract_data_from_csv
    )
    task8=PythonOperator(
        task_id="extract_data_from_tsv",
        python_callable=extract_data_from_tsv
    
    )
    task9=PythonOperator(
        task_id="extract_data_from_fixed_width",
        python_callable=extract_data_from_fixed_width
    
    )
    task10=PythonOperator(
        task_id="merge_csv_files",
        python_callable=merge_csv_files
    
    )
    task11=PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    
    )
    task12=PythonOperator(
        task_id="uploadmergedfile_to_s3",
        python_callable=uploadmergedfile_to_s3
    
    )
    # task1>>task2
    # task2>>task3
    task2>>task3>>task4>>task5 >>task6 >>task7>>task8>>task9>>task10>>task11>>task12
