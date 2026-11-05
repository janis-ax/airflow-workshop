"""
Musterlösung Aufgabe 5: Pool anlegen und nutzen

Voraussetzung: In der UI unter Admin > Pools einen Pool
"workshop_pool" mit 2 Slots anlegen.

Drei Tasks teilen sich den Pool. Im Grid oder Gantt sieht man:
Es laufen nie mehr als zwei gleichzeitig, der dritte wartet (Status: queued/scheduled).
"""

from __future__ import annotations

import time

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="loesung_05_pool",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["musterloesung", "aufgabe_05"],
)
def pool_demo():
    @task(pool="workshop_pool")
    def verarbeite(nummer: int):
        print(f"Task {nummer} startet")
        time.sleep(30)
        print(f"Task {nummer} fertig")

    # Drei Aufrufe derselben Funktion. Gleiche Funktion, mehrere Tasks:
    # die task_id wird dafür mit override() gesetzt.
    for i in range(1, 4):
        verarbeite.override(task_id=f"verarbeite_{i}")(i)


pool_demo()
