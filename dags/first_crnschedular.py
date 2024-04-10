"""
A CRON expression is a string comprising five fields separated by white space that represents a set of times

normally as a schedule to execute some routine.
15 minute
14 hour
1 day
* month 
* week    

today date: 4-2-2024
cron expression: 5 4 * * *  # this will run at 4:05 am every day


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
    dag_id="first_cron",
    description="this is my first cron job",
    start_date=datetime(2024,3,27),
    default_args=default_args,
    schedule_interval="5 4 * * *"   


) as dag:
    task1=BashOperator(
        task_id="first_task",
        bash_command="echo hello world, this is my first task"
    )
    task2=BashOperator(
        task_id="second_task",
        bash_command="echo hello world, this is my second task"
    )
    task3=BashOperator(
        task_id="third_task",
        bash_command="echo hello world, this is my third task"
    )
    task1 >> task2 >> task3