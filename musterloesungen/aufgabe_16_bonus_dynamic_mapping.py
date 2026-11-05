"""
Musterlösung Aufgabe 16 (Bonus): Dynamic Task Mapping

Statt chunk_1, chunk_2, chunk_3 fest zu schreiben, erzeugt Airflow
zur Laufzeit so viele Task-Instanzen, wie es Chunks gibt.
Die Anzahl kann sich also von Run zu Run ändern.
"""

from __future__ import annotations

import time
from datetime import timedelta

import pendulum
from airflow.sdk import Param, dag, task


@dag(
    dag_id="loesung_16_bonus_dynamic_mapping",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    params={"anzahl_chunks": Param(5, type="integer", minimum=1, maximum=20)},
    tags=["musterloesung", "aufgabe_16", "bonus"],
)
def long_running_mapping():
    @task
    def plane_chunks(params=None) -> list[int]:
        return list(range(1, params["anzahl_chunks"] + 1))

    @task(execution_timeout=timedelta(minutes=5))
    def verarbeite_chunk(chunk: int):
        print(f"Chunk {chunk} startet")
        time.sleep(20)
        print(f"Chunk {chunk} fertig")

    @task
    def finish():
        print("Alle Chunks verarbeitet")

    # expand() erzeugt eine Task-Instanz pro Listenelement
    verarbeite_chunk.expand(chunk=plane_chunks()) >> finish()


long_running_mapping()
