from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
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
    dag_id="etl_data",
    default_args=default_args,
    start_date=datetime(2024,3,31,2),
    schedule_interval="@daily",
    description="this is my first dag building with python operator"



) as dag:
    

    


    
    zip_file_path="../data/tolldata.tgz"
    def extract_process_started():
        cwd = os.getcwd()
        return cwd
    def unzip_file():

        try:
            # Open the tgz file for reading
            with tarfile.open(zip_file_path, 'r:gz') as tar:
                # Extract all the contents into the specified directory
                tar.extractall("../dummy")
            print("Extraction complete.")
        except FileNotFoundError:
            print(f"Error: File {zip_file_path} not found.")
        except tarfile.ReadError:
            print(f"Error: Unable to open or read the file {zip_file_path}.")
        except tarfile.CompressionError:
            print(f"Error: Unable to decompress the file {zip_file_path}.")
        except tarfile.TarError:
            print(f"Error: An error occurred while extracting the file {zip_file_path}.")
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")

    
    def extract_data_from_text(file_path="../data/tolldata/fileformats.txt"):
        if os.path.exists(file_path):
            with open(file_path) as f:
                return f.read()
        else:
            return "file does not exist"
   

    def extract_data_from_csv():
        # Initialize an empty list to store the modified data
        modified_data = []
        cwd = os.getcwd()
        print(cwd)
        full_folder_path = os.path.join(cwd, "../data/tolldata")
        # full_folder_path = os.path.join(cwd, folder_path)

        # Check if the folder exists
        if os.path.exists(full_folder_path) and os.path.isdir(full_folder_path):
            # Create the extraction_done folder if it doesn't exist
            extraction_done_folder = os.path.join(cwd, "../extraction_done")
            print(extraction_done_folder)
            final_path = os.path.join(cwd, "../destination")
            os.makedirs(extraction_done_folder, exist_ok=True)


            # List all files in the folder
            files = os.listdir(full_folder_path)
            
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
                                time.strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
                                row[0],  # Anonymized Vehicle number (assuming it's the first column)
                                row[1],  # Vehicle type (assuming it's the second column)
                            ]
                            # Append the modified row to the list
                            modified_data.append(modified_row)

                    # Move the source CSV file to the extraction_done folder
                    
                    shutil.move(file_path, extraction_done_folder)
                    print(f"Moved {file} to extraction_done folder.")

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

    def extract_data_from_tsv(folder_path="../data/tolldata"):
    # Initialize an empty list to store the modified data
        modified_data = []

        # Check if the folder exists
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Create the extraction_done folder if it doesn't exist
            extraction_done_folder = "../extraction_done"
            final_path="../destination"
            os.makedirs(extraction_done_folder, exist_ok=True)

            # List all files in the folder
            files = os.listdir(folder_path)
            
            # Initialize a counter to keep track of the number of tSV files
            tsv_count = 0
            
            # Iterate over the files
            for file in files:
                # Check if the file is a tSV file
                if file.endswith(".tsv"):
                    # Increment the CSV file counter
                    tsv_count += 1
                    
                    # Construct the full path to the tSV file
                    file_path = os.path.join(folder_path, file)

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
                    
                    shutil.move(file_path, extraction_done_folder)
                    print(f"Moved {file} to extraction_done folder.")

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
            print(f"Folder {folder_path} does not exist.")
    
    def extract_data_from_fixed_width(folder_path="../data/tolldata"):
        # Initialize an empty list to store the modified data
        modified_data = []

        # Check if the folder exists
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Create the extraction_done folder if it doesn't exist
            extraction_done_folder = "../extraction_done"
            final_path="../destination"
            os.makedirs(extraction_done_folder, exist_ok=True)

            # List all files in the folder
            files = os.listdir(folder_path)
            
            # Initialize a counter to keep track of the number of txt files
            txt_count = 0
            colspecs = [(0, 6), (6, 32), (33, 43), (43, 48), (49, 60), (57, 61), (61, 70)]

        # Define column names
            column_names = ["Column1", "Column2", "Column3", "Column4", "Column5", "Type of Payment code", "Vehicle Code code"]
            
            # Iterate over the files
            for file in files:
                # Check if the file is a txt file
                if file.endswith(".txt"):
                    # Increment the CSV file counter
                    txt_count += 1
                    
                    # Construct the full path to the txt file
                    file_path = os.path.join(folder_path, file)

                    # Read the contents of the txt file
                    with open(file_path, 'r') as f:
                        # Skip the header line
                        # next(f)
                        df = pd.read_fwf(f, colspecs=colspecs, header=None, names=column_names)
                        extracted_df = df[["Type of Payment code", "Vehicle Code code"]]
                        # Write the renamed data to a CSV file
                        extracted_df.to_csv(final_path+"/txt_data.csv", index=False)

                    # Move the source txt file to the extraction_done folder
                    
                    shutil.move(file_path, extraction_done_folder)
                    print(f"Moved {file} to extraction_done folder.")

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
            print(f"Folder {folder_path} does not exist.")


        
    
    def transform():
        return "transforming data"
    
    def load():
        return "loading data"
    
    task1=PythonOperator(
        task_id="extract_process_started",
        python_callable=extract_process_started )
    
    task2=PythonOperator(
        task_id="extract_data_from_text",
        python_callable=extract_data_from_text)
    task3=PythonOperator(
        task_id="extract_data_from_csv",
        python_callable=extract_data_from_csv)
    task4=PythonOperator(
        task_id="extract_data_from_tsv",
        python_callable=extract_data_from_tsv)
    task5=PythonOperator(
        task_id="extract_data_from_fixed_width",
        python_callable=extract_data_from_fixed_width)
    
    task6=PythonOperator(
        task_id="transform",
        python_callable=transform)
    
    task7=PythonOperator(
        task_id="load",
        python_callable=load)
    task8=BashOperator(
        task_id="combine_files",
        bash_command="cat ../destination/csv_data.csv ../destination/tsv_data.csv ../destination/txt_data.csv > ../destination/combined_data.csv"
    )
    

    task1>>task2>>task3 >>task4>>task5>>task6>>task7