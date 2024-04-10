from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
#pache-airflow-providers-postgres        5.10.2
default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id="dagwithpostgres",
    start_date=datetime(2024, 3, 31, 2),
    schedule_interval="5 4 * * *",
    description="This is my first DAG building with Python Operator"
) as dag:
    task1=PostgresOperator(
    task_id="create_table",
    postgres_conn_id="postgress_localhost",
    sql="""
    CREATE TABLE IF NOT EXISTS dag_runs (
            dt DATE,
            dag_id VARCHAR(250),
            timestamp TIMESTAMP,
            unique_num INT)
           
    """
    )
    task2=PostgresOperator(
    task_id="insert_data",
    postgres_conn_id="postgress_localhost",
    sql="""
    INSERT INTO dag_runs (dt, dag_id, timestamp, unique_num) VALUES ('{{ ds }}', '{{ dag.dag_id }}', '{{ execution_date }}', {{ task_instance_key_str.split('_')[-1] }})
    
    """
    )
    # task3=PostgresOperator(
    # task_id="delete_data",
    # postgres_conn_id="postgress_localhost",
    # sql="""
    # DELETE FROM dag_runs WHERE dt='{{ ds }}' AND dag_id='{{ dag.dag_id }}'
    # """
    # )
    task4=PostgresOperator(
        task_id="read_data",
        postgres_conn_id="postgress_localhost",
        sql="""
        SELECT * FROM dag_runs
        """



    )
    task1 >>task2>>task4
    