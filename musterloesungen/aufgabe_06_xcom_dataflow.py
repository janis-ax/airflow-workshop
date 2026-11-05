"""
Musterlösung Aufgabe 6: XCom Dataflow

produce_data gibt ein Dict zurück (wird automatisch als XCom gespeichert),
consume_data bekommt es als normalen Parameter.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task


@dag(
    dag_id="loesung_06_xcom_dataflow",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["musterloesung", "aufgabe_06"],
)
def xcom_dataflow():
    @task
    def produce_data() -> dict:
        return {"user": "ish", "score": 42}

    @task
    def consume_data(data: dict):
        print(f"User {data['user']} hat Score {data['score']}")

    log_date = BashOperator(
        task_id="log_date",
        bash_command='echo "Run {{ logical_date | ds }}"',
    )

    # Der Aufruf consume_data(produce_data()) erzeugt die Abhängigkeit
    # produce_data >> consume_data automatisch.
    consume_data(produce_data()) >> log_date


xcom_dataflow()
