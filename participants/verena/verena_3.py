from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
import pendulum 
from airflow.sdk import get_current_context
import os
from verena.utils import number1, number2, number3

def eins_plus_zwei(zahl1, zahl2):
    return zahl1 + zahl2



@dag(
    dag_id="verena_3",
    schedule="20 * * * *",
    start_date=pendulum.datetime(2026, 11, 5, 12, 0, tz="Europe/Berlin"),
    catchup=False,
    max_active_tasks=1,
    tags=["test", "verena"]
)
def mein_dag():


    addition_task = PythonOperator(task_id = eins_plus_zwei, callable=eins_plus_zwei)

    addition_task

mein_dag()