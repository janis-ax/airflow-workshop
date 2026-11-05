"""
Beispiel 10: Dynamic Task Mapping

expand() erzeugt zur Laufzeit eine Task-Instanz pro Element einer Liste.
Die Anzahl muss beim Schreiben des DAGs nicht bekannt sein.
partial() setzt Werte, die für alle Instanzen gleich sind.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task


@dag(
    dag_id="beispiel_10_dynamic_task_mapping",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "mapping"],
)
def dynamic_task_mapping():
    @task
    def finde_dateien() -> list[str]:
        # In echt z. B.: Dateien in einem S3-Bucket auflisten
        return ["umsatz_nord.csv", "umsatz_sued.csv", "umsatz_west.csv"]

    @task
    def verarbeite(datei: str, trennzeichen: str) -> int:
        print(f"Verarbeite {datei} (Trennzeichen '{trennzeichen}')")
        return len(datei)

    @task
    def summiere(ergebnisse: list[int]):
        # Bekommt automatisch die Ergebnisse ALLER Instanzen
        print(f"{len(list(ergebnisse))} Dateien verarbeitet, Summe {sum(ergebnisse)}")

    dateien = finde_dateien()
    ergebnisse = verarbeite.partial(trennzeichen=";").expand(datei=dateien)
    summiere(ergebnisse)

    # Mapping geht auch mit klassischen Operatoren
    BashOperator.partial(task_id="bash_pro_datei").expand(
        bash_command=["echo nord", "echo sued", "echo west"]
    )


dynamic_task_mapping()
