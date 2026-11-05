"""
Beispiel 02: Der klassische Stil mit "with DAG" und Operatoren

So sieht viel bestehender Airflow-Code aus. Funktioniert genauso gut,
ist aber etwas länger als TaskFlow (siehe Beispiel 01).
"""

from __future__ import annotations

from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG


def begruessung(name: str):
    print(f"Hallo {name}!")


with DAG(
    dag_id="beispiel_02_klassisch_operatoren",
    description="BashOperator, PythonOperator und EmptyOperator im klassischen Stil",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
    tags=["beispiel", "grundlagen"],
):
    start = EmptyOperator(task_id="start")

    datum = BashOperator(
        task_id="zeige_datum",
        bash_command='echo "Heute ist {{ logical_date | ds }}"',
    )

    hallo = PythonOperator(
        task_id="sag_hallo",
        python_callable=begruessung,
        op_kwargs={"name": "Workshop"},
    )

    ende = EmptyOperator(task_id="ende")

    start >> datum >> hallo >> ende
