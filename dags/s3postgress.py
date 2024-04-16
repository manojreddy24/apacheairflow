from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
import csv
import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
#pache-airflow-providers-postgres        5.10.2
default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5)
}
with DAG(
    dag_id="s3postgress",
    default_args=default_args,
    description="s3 with minions",
    start_date=datetime(2022, 3, 31),
    schedule_interval="0 0 * * *",





) as dag:
    def postgresstos3(pastd="2017-07-10", newd="2017-07-30"):
        hook=PostgresHook(postgres_conn_id="postgress_localhost")
        connection=hook.get_conn()
        cursor=connection.cursor()
        file_name=f"dags/get_orders{pastd}.txt"
        cursor.execute("SELECT * FROM orders where order_date >= DATE '2017-06-12' and order_date<= DATE '2017-07-20'")
        with open(f"dags/get_orders{newd}.txt", "w") as f:
            csv_writer=csv.writer(f)
            csv_writer.writerows(i[0] for i in cursor.description)
            csv_writer.writerows(cursor)
        cursor.close()
        connection.close()
        logging.info("Data has been written to the file: %s", file_name)
        s3_hook=S3Hook(aws_conn_id="minin_s3")
        s3_hook.load_file(
            filename="dags/get_orders2017-07-20.txt",
            key="orders/"+newd+".txt",
            bucket_name="airflow",
            replace=True
    )
    task1=PythonOperator(
        task_id="postgresstos3",
        python_callable=postgresstos3,
    

    )
   
    