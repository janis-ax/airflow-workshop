"""
Musterlösung Aufgabe 18: Wiederholung Parallele Datenverarbeitung

Voraussetzung: Pool "verarbeitung_pool" mit 2 Slots (Admin > Pools).

Beobachtungen:
- Von den drei Lade-Tasks laufen nur zwei gleichzeitig (Pool mit 2 Slots).
- Schlägt ein Lade-Task fehl, läuft zusammenfuehren trotzdem,
  weil trigger_rule="all_done" nur "alle Vorgänger fertig" verlangt.
  report läuft danach normal, weil zusammenfuehren erfolgreich war.

Zum Testen des Fehlerfalls beim Triggern {"fehler_in": "json"} mitgeben.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import Param, dag, get_current_context, task


@dag(
    dag_id="loesung_18_parallele_verarbeitung",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    params={
        "fehler_in": Param(
            "keiner",
            type="string",
            enum=["keiner", "csv", "json", "xml"],
            description="Welcher Lade-Task soll absichtlich fehlschlagen?",
        )
    },
    tags=["musterloesung", "aufgabe_18"],
)
def parallele_verarbeitung():
    start = EmptyOperator(task_id="start")

    @task(pool="verarbeitung_pool")
    def laden(format_: str):
        if get_current_context()["params"]["fehler_in"] == format_:
            raise Exception(f"Simulierter Fehler beim Laden von {format_.upper()}")
        print(f"{format_.upper()} geladen")

    @task(trigger_rule="all_done")
    def zusammenfuehren():
        print("Alle Quellen zusammengeführt")

    report = BashOperator(
        task_id="report",
        bash_command='echo "Report erstellt am {{ logical_date | ds }}"',
    )

    lade_tasks = [laden.override(task_id=f"laden_{f}")(f) for f in ["csv", "json", "xml"]]
    start >> lade_tasks >> zusammenfuehren() >> report


parallele_verarbeitung()
