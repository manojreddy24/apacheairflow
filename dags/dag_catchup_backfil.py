"""
Catchup:
If catchup=True, Airflow will automatically schedule and execute DAG runs for all the intervals between the DAG's start_date and the current date, even if those intervals have already passed. This means that Airflow will "catch up" on any missed DAG runs.
If catchup=False, Airflow will only schedule and execute DAG runs for intervals that have not yet occurred. It will not "catch up" on missed DAG runs.

Backfill:
Backfilling refers to the process of manually triggering DAG runs for historical data that was not processed when the DAG was initially created.
Backfilling is often used in conjunction with catchup=False or for reprocessing historical data.
o backfill DAG runs, you can use the Airflow CLI command airflow dags backfill <dag_id> -s <start_date> -e <end_date>.
This command triggers DAG runs for each interval between the specified start_date and end_date, even if those intervals have already passed.

"""


from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
default_args={
    "owner":"airflow",
    "retries":3,
    "retry_delay": timedelta(minutes=5)


}
with DAG(
    dag_id="first_catchupbackfill",
    start_date=datetime(2024,3,27),
    default_args=default_args,
    description="this is my first catchup and backfill dag building",
    schedule_interval="@daily",
    catchup=True

) as dag:
     task1=BashOperator(
            task_id="first_task",
            bash_command="echo hello world, this is my first task"
        )
       

#docker exec -it f49953fd98a6 bash
     #wil go to new bash id
#airflow dags backfill -s 2024-03-27 -e 2024-03-30 first_catchupbackfill
     #exit to get back to our terminal