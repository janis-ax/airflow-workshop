"""
Musterlösung Aufgabe 4: Fan-In mit Trigger Rule

Struktur: A >> [B, C] >> D
B schlägt absichtlich fehl. D läuft trotzdem, weil trigger_rule="all_done"
nur verlangt, dass alle Vorgänger FERTIG sind (egal ob erfolgreich oder nicht).
"""

from __future__ import annotations

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="loesung_04_fan_in_trigger_rule",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["musterloesung", "aufgabe_04"],
)
def fan_in_trigger_rule():
    @task
    def a():
        print("A: Start")

    @task
    def b():
        print("B: Ich schlage jetzt absichtlich fehl")
        raise Exception("Simulierter Fehler in Task B")

    @task
    def c():
        print("C: Erfolgreich")

    @task(trigger_rule="all_done")
    def d():
        # Mit der Standardregel "all_success" würde D hier
        # den Status upstream_failed bekommen und nicht laufen.
        print("D: Ich laufe trotzdem, weil alle Vorgänger fertig sind")

    task_a = a()
    task_a >> [b(), c()] >> d()


fan_in_trigger_rule()
