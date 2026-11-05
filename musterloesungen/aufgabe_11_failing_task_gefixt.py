"""
Musterlösung Aufgabe 11: Failing Task analysieren

Ausgangslage: aufgaben/vorlagen/vorlage_11_failing_task.py
Dort wirft failing_task bei jedem Lauf einen RuntimeError.

Vorgehen:
1. Run starten, Task wird rot (nach einem Retry)
2. Log öffnen: Der Stacktrace zeigt Datei, Zeile und die Meldung
   "RuntimeError: Demo failure ... (intentional)"
3. Ursache beheben: Die Exception entfernen und echte Logik einbauen
4. Neu deployen und erneut testen: Alle Tasks werden grün

Zusätzlich zeigt die Lösung, wie man Fehler sinnvoll behandelt:
Erwartbare Probleme werden geprüft und mit einer klaren Meldung abgebrochen.
"""

from __future__ import annotations

from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task


@dag(
    dag_id="loesung_11_failing_task_gefixt",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["musterloesung", "aufgabe_11"],
)
def failing_task_gefixt():
    @task
    def failing_task() -> int:
        # Vorher: raise RuntimeError("Demo failure ...")
        # Nachher: echte Arbeit, die einen Wert zurückgibt
        datensaetze = [1, 2, 3]
        if not datensaetze:
            # Fehler mit klarer Meldung statt einer unklaren Exception
            raise ValueError("Keine Datensätze gefunden, bitte Quelle prüfen")
        print(f"{len(datensaetze)} Datensätze verarbeitet")
        return len(datensaetze)

    @task
    def inspect_context(anzahl: int):
        print(f"DAG ist wieder gesund, {anzahl} Datensätze verarbeitet")

    log_run = BashOperator(
        task_id="log_run",
        bash_command='echo "Run {{ run_id }} beendet um {{ ts }}"',
        trigger_rule="all_done",
    )

    inspect_context(failing_task()) >> log_run


failing_task_gefixt()
