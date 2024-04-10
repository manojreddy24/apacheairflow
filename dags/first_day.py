from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
default_args={
"owner":"airflow",
"retries":3,
"retry_delay": timedelta(minutes=5)
}
with DAG(
    dag_id="first_dag_bitwise3",
    default_args=default_args,
    description="this is my first dag building",
    start_date=datetime(2024,3,31,2),
    schedule_interval="@daily"

) as dag:
    task1=BashOperator(
        task_id="first_task",
        bash_command="echo hello world, this is my first task",



    )
    task2=BashOperator(
        task_id="second_task",
        bash_command="echo hello world, this is my second task",

    )
    taks3=BashOperator(
        task_id="third_task",
        bash_command="echo hello world, this is my third task"
    )
    #task dependency method 1
    # task1.set_downstream(task2) # task1 will run first then task2
    # task1.set_downstream(taks3) # task1 will run first then task3
    # task2.set_downstream(task1) # task2 will run first then task1   only  task2 will run after success of task1
   # task dependency method 2
    #or use bitwise oprators

    # task1 >> task2
    # task1 >> taks3
#task dependency method 3
    task1>>[task2,taks3] # task1 will run first then task2 and task3
