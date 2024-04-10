from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.decorators import task, dag
from datetime import datetime, timedelta
default_args={
    "owner":"airflow",
    "retries":3,
    "retry_delay": timedelta(minutes=5)
    
}
@dag(

    default_args=default_args,
    dag_id="first_taskflow",
    start_date=datetime(2024,3,31,2),
    schedule_interval="@daily",
    description="this is my first dag building with python operator"
)
def hello_worldetl():
    @task(multiple_outputs=True)
    def fullname():
       return{
           "first_name":"manoj reddy",
              "last_name":"avula"
       }

    @task
    def greet():
        return "hello world"
    @task
    def name(name):
        print(f"hello {name}")
        return name
    @task
    def age(age):
        return age
    
    @task
    def details(name,age,first_name,last_name  ):
        print(f"name is {name} and age is {age}")
        print(f"full name is {first_name} {last_name}  and age is {age}")
   

    greet= greet()
    age=age(25)
    name=name("manoj")
    fullname_task=fullname()
    details=details(name,age,fullname_task["first_name"],fullname_task["last_name"])
hello_worl=hello_worldetl()

