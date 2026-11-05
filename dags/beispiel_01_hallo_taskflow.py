"""
Beispiel 01: Der kleinste sinnvolle DAG im Decorator-Stil (TaskFlow)

- @dag macht aus einer Funktion einen DAG, der Funktionsname wird zur dag_id
- @task macht aus einer Funktion einen Task, der Funktionsname wird zur task_id
- Der Aufruf am Ende (hallo_taskflow()) registriert den DAG
"""

from __future__ import annotations

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="beispiel_01_hallo_taskflow",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,  # nur manuell starten
    catchup=False,
    tags=["beispiel", "grundlagen"],
)
def hallo_taskflow():
    @task
    def sag_hallo() -> str:
        print("Hallo Airflow!")
        return "Hallo"

    @task
    def sag_tschuess(gruss: str):
        print(f"{gruss} war gestern, jetzt: Tschüss!")

    # Daten weitergeben = Abhängigkeit setzen
    sag_tschuess(sag_hallo())


hallo_taskflow()
