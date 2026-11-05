"""
Musterlösung Aufgabe 22: DAG, der den eigenen HttpStatusTrigger nutzt.

Beobachten: Der Task wechselt in den Status "deferred".
Im Log des Triggerers sieht man die periodischen Abfragen.
"""

from __future__ import annotations

import pendulum
from airflow.sdk import Param, dag, task

from musterloesungen.aufgabe_22_custom_trigger.http_status_trigger import (
    WaitForHttpStatusOperator,
)


@dag(
    dag_id="loesung_22_custom_trigger",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    params={"url": Param("https://airflow.apache.org", type="string")},
    tags=["musterloesung", "aufgabe_22", "deferrable"],
)
def custom_trigger_demo():
    warte = WaitForHttpStatusOperator(
        task_id="warte_auf_status",
        url="{{ params.url }}",
        expected_status_code=200,
        poke_interval=15,
        wait_timeout=300,
    )

    @task
    def weiter(status_code: int):
        print(f"Service ist erreichbar, Status {status_code}")

    weiter(warte.output)


custom_trigger_demo()
