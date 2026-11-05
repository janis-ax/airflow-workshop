"""
Beispiel 08: Robustheit mit Retries, Timeouts und Callbacks

- retries / retry_delay / retry_exponential_backoff: automatisch neu versuchen
- execution_timeout: Task wird abgebrochen, wenn er zu lange läuft
- dagrun_timeout: ganzer DAG Run wird abgebrochen
- on_failure_callback: Funktion, die bei Fehlern aufgerufen wird (z. B. Mail, Teams)
"""

from __future__ import annotations

import random
from datetime import timedelta

import pendulum
from airflow.sdk import dag, task


def melde_fehler(context):
    ti = context["ti"]
    print(f"ALARM: {ti.dag_id}.{ti.task_id} ist fehlgeschlagen (Versuch {ti.try_number})")


@dag(
    dag_id="beispiel_08_retries_timeouts_callbacks",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(minutes=30),
    default_args={
        "retries": 3,
        "retry_delay": timedelta(seconds=10),
        "retry_exponential_backoff": True,  # 10s, 20s, 40s ...
        "execution_timeout": timedelta(minutes=5),
        "on_failure_callback": melde_fehler,
    },
    tags=["beispiel", "robustheit"],
)
def robustheit():
    @task
    def wackelige_api() -> int:
        # Schlägt in etwa der Hälfte der Fälle fehl, Retries fangen das ab
        if random.random() < 0.5:
            raise ConnectionError("API nicht erreichbar")
        return 200

    @task(retries=0)  # Retries pro Task überschreiben
    def verarbeite(status: int):
        print(f"API-Status {status}, Verarbeitung läuft")

    verarbeite(wackelige_api())


robustheit()
