When you extract the zip file you should see the following 3 files.

Filelist:

vehicle-data.csv
tollplaza-data.tsv
payment-data.txt

vehicle-data.csv:

vehicle-data.csv is a comma-separated values file.
It has the below 6 fields

Rowid  - This uniquely identifies each row. This is consistent across all the three files.
Timestamp - What time did the vehicle pass through the toll gate.
Anonymized Vehicle number - Anonymized registration number of the vehicle 
Vehicle type - Type of the vehicle
Number of axles - Number of axles of the vehicle
Vehicle code - Category of the vehicle as per the toll plaza.


tollplaza-data.tsv:
tollplaza-data.tsv is a tab-separated values file.
It has the below 7 fields

Rowid  - This uniquely identifies each row. This is consistent across all the three files.
Timestamp - What time did the vehicle pass through the toll gate.
Anonymized Vehicle number - Anonymized registration number of the vehicle 
Vehicle type - Type of the vehicle
Number of axles - Number of axles of the vehicle
Tollplaza id - Id of the toll plaza
Tollplaza code - Tollplaza accounting code.

payment-data.txt:

payment-data.txt is a fixed width file. Each field occupies a fixed number of characters.

It has the below 7 fields

Rowid  - This uniquely identifies each row. This is consistent across all the three files.
Timestamp - What time did the vehicle pass through the toll gate.
Anonymized Vehicle number - Anonymized registration number of the vehicle 
Tollplaza id - Id of the toll plaza
Tollplaza code - Tollplaza accounting code.
Type of Payment code - Code to indicate the type of payment. Example : Prepaid, Cash.
Vehicle Code -  Category of the vehicle as per the toll plaza.









Summary of each function:

1. **upload_to_s3**: This function uploads a file named "tolldata.tgz" to an AWS S3 bucket under the path "orders/tolldata.tgz". It replaces any existing file with the same name.

2. **downloading_from_s3**: This function downloads a file named "orders/tolldata.tgz" from an AWS S3 bucket and saves it locally. It then returns the local path where the file is saved.

3. **change_extension_to_tgz**: This function iterates through files in a directory, changes the extension of files starting with "airflow_tmp" to ".tgz", and prints the name of the file and the change made.

4. **create_directory**: This function creates a directory named "data" in the parent directory of the current script if it doesn't already exist.

5. **extract_files**: This function extracts files from a .tgz file to the "data" directory. It prints messages indicating the success or failure of the extraction process.

6. **delete_files_with_dot_prefix**: This function deletes files with names starting with a dot (.) in the "data" directory. It also deletes a specific file named "fileformats.txt" if it exists.

7. **extract_data_from_csv**: This function reads CSV files from the "data" directory, extracts specific columns, and writes the modified data to a new CSV file named "csv_data.csv" in the "destination" directory.

8. **extract_data_from_tsv**: This function reads TSV files from the "data" directory, extracts specific columns, and writes the modified data to a new CSV file named "tsv_data.csv" in the "destination" directory.

9. **extract_data_from_fixed_width**: This function reads fixed-width format (txt) files from the "data" directory, extracts specific columns, and writes the modified data to a new CSV file named "txt_data.csv" in the "destination" directory.

10. **merge_csv_files**: This function merges CSV files "csv_data.csv", "tsv_data.csv", and "txt_data.csv" from the "destination" directory into a single CSV file named "merged.csv" in the same directory.

11. **transform_data**: This function reads the merged CSV file "merged.csv" from the "destination" directory, transforms the data by converting the "Vehicle type" column to uppercase, and writes the transformed data to a new CSV file named "transformed_data.csv" in the same directory.

12. **uploadmergedfile_to_s3**: This function uploads the transformed CSV file "transformed_data.csv" from the "destination" directory to an AWS S3 bucket under the path "orders/transformed_data.csv". It replaces any existing file with the same name.
