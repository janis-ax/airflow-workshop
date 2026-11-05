from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(
    dag_id="tobi3",
    tags=["test", "test2", "test3"],
    schedule="@daily",
    start_date=2026-11-1,
    catchup=False
)
def mydag():
    @task
    def doing_1():
        print("Hello")

    @task
    def doing_2():
        print("World")

    @task.bash
    def doing_3()-> str:
        return "sleep 30"

    doing_1 >> doing_3 >> doing_2

mydag()