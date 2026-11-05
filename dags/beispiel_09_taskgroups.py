"""
Beispiel 09: TaskGroups

TaskGroups fassen zusammengehörige Tasks in der UI zu einem aufklappbaren
Block zusammen. Sie sind der Ersatz für die entfernten SubDAGs.
Die task_id bekommt den Gruppennamen als Präfix, z. B. "quelle_a.laden".
"""

from __future__ import annotations

import pendulum
from airflow.sdk import dag, task, task_group


@dag(
    dag_id="beispiel_09_taskgroups",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "taskgroup"],
)
def taskgroups():
    @task
    def start():
        print("Start")

    @task_group
    def verarbeite_quelle(name: str):
        @task
        def laden(quelle: str) -> str:
            print(f"Lade {quelle}")
            return quelle

        @task
        def pruefen(quelle: str):
            print(f"Prüfe {quelle}")

        pruefen(laden(name))

    @task
    def zusammenfuehren():
        print("Alle Quellen fertig, führe zusammen")

    # Gibt die Gruppen-Funktion nichts zurück, liefert der Aufruf die TaskGroup.
    # Pfeile auf eine TaskGroup gelten für den ersten bzw. letzten Task darin.
    gruppen = [verarbeite_quelle.override(group_id=f"quelle_{q}")(q) for q in ["a", "b", "c"]]
    start() >> gruppen >> zusammenfuehren()


taskgroups()
