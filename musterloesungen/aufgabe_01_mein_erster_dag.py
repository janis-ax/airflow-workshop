"""
Musterlösung Aufgabe 1: Mein erster DAG

Ein DAG im Decorator-Stil (TaskFlow) mit zwei klassischen BashOperatoren
und einer @task-Funktion dazwischen.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task


@dag(
    dag_id="loesung_01_mein_erster_dag",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="@daily",
    catchup=False,
    tags=["musterloesung", "aufgabe_01"],
)
def mein_erster_dag():
    start = BashOperator(
        task_id="start",
        bash_command='echo "Start"',
    )

    @task
    def process():
        print("Processing...")

    end = BashOperator(
        task_id="end",
        bash_command='echo "End"',
    )

    # process ist eine Funktion: erst der Aufruf process() erzeugt den Task
    start >> process() >> end


mein_erster_dag()
