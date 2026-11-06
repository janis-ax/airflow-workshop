from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
import pendulum 
from airflow.sdk import get_current_context
import os






@dag(
    dag_id="verena_3",
    schedule="20 * * * *",
    start_date=pendulum.datetime(2026, 11, 5, 12, 0, tz="Europe/Berlin"),
    catchup=False,
    max_active_tasks=1,
    tags=["test", "verena"]
)
def mein_dag():

    @task
    def number1():
        print("hallo")

        number1 = 1
        return number1

    @task
    def number2():
        number2 = 2
        return number2

    @task
    def addition():
        context = get_current_context()
        ti = context["ti"]

        wert1 = ti.xcom_pull(task_ids="number1")
        wert2 = ti.xcom_pull(task_ids="number2")

        ergebnis = wert1 + wert2

        print(f"Ergebnis: {ergebnis}")

        return ergebnis

    # Task-Abhängigkeiten
    n1 = number1()
    n2 = number2()

    addition_task = addition()

    [n1, n2] >> addition_task