
from airflow.sdk import dag
from airflow.providers.standard.operators.python import PythonOperator
import pendulum

from participants.verena.utils.verena_lib import number1, number2

def eins_plus_zwei():
    return number1 + number2


def eins_minus(**context):
    ti = context["ti"]

    ergebnis_addition = ti.xcom_pull(
        task_ids="addition_task"
    )

    return ergebnis_addition - number1


@dag(
    dag_id="verena_3",
    schedule="20 * * * *",
    start_date=pendulum.datetime(
        2026, 11, 5, 12, 0, tz="Europe/Berlin"
    ),
    catchup=False,
    max_active_tasks=1,
    tags=["test", "verena"]
)
def mein_dag():

    addition_task = PythonOperator(
        task_id="addition_task",
        python_callable=eins_plus_zwei
    )

    subtraction_task = PythonOperator(
        task_id="subtraction_task",
        python_callable=eins_minus
    )

    addition_task >> subtraction_task


mein_dag()
