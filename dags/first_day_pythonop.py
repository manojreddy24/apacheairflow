from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
default_args={
    "owner":"airflow",
    "retries":3,
    "retry_delay": timedelta(minutes=5)
    
}


with DAG(
    default_args=default_args,
    dag_id="first_dag_pythonop",
    start_date=datetime(2024,3,31,2),
    schedule_interval="@daily",
    description="this is my first dag building with python operator"




) as dag:
    
    def greet():
        return "hello world"
    def name(name):
        print(f"hello {name}")
        return name  # need to use return to pass the value to next task
    def details(age,ti):# ti is for task instance
        name=ti.xcom_pull(task_ids="name")
        first_name=ti.xcom_pull(key="first_name",task_ids="fullname")
        last_name=ti.xcom_pull(key="last_name",task_ids="fullname")
        print(f"name is {name} and age is {age}")
        print(f"full name is {first_name} {last_name}  and age is {age}")
        return age  # just dispaying in xcom
        # return f"name is {name} and age is {age}"
    def fullname(ti):
        first_name=ti.xcom_push(key="first_name",value="manoj reddy")
        last_name=ti.xcom_push(key="last_name",value="avula")

    
    task1=PythonOperator(
        task_id="first_task",
        python_callable=greet )
    task2=PythonOperator(
        task_id="name",
        python_callable=name,
        op_args=["manoj"],# op_args={"name":"manoj"}
        provide_context=True  # Passes the context to the callable function
    )
    task3=PythonOperator(
        task_id="details",
        python_callable=details,
        op_kwargs={"age":25},
        provide_context=True  # Passes the context to the callable function
        )
    task4=PythonOperator(
        task_id="fullname",
        python_callable=fullname)
    task1>>task2>>task4>>task3
    # task1>>task2>>task4>>task3 if you execute this way it will fail because task3 is dependent on task4 so it will not get the value from task4 so it will fail
    # task3>>task2>>task1


    #benifts of using x_coms it is used to communicate between tasks 
    #maximum size of xcom is 48kb very less so we can use it for small data
    #we can reduce the lines of code using taskflow api

