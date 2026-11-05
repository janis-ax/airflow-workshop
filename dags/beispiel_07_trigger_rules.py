"""
Beispiel 07: Trigger Rules

Standard ist "all_success": ein Task läuft nur, wenn alle Vorgänger erfolgreich waren.
Andere Regeln sind nützlich für Aufräumen, Benachrichtigungen oder Joins.

Hier schlägt "instabil" absichtlich fehl. Im Grid sieht man, welche Tasks
trotzdem laufen und welche upstream_failed werden.
"""

from __future__ import annotations

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="beispiel_07_trigger_rules",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "trigger_rules"],
)
def trigger_rules():
    @task
    def stabil():
        print("Läuft durch")

    @task
    def instabil():
        raise Exception("Absichtlicher Fehler")

    @task  # all_success (Standard): wird upstream_failed
    def nur_bei_erfolg():
        print("Läuft nicht, weil instabil fehlgeschlagen ist")

    @task(trigger_rule="all_done")  # läuft immer, wenn alle fertig sind
    def aufraeumen():
        print("Temporäre Dateien löschen")

    @task(trigger_rule="one_failed")  # läuft, sobald einer fehlschlägt
    def alarm():
        print("Benachrichtigung: Es ist etwas schiefgegangen")

    @task(trigger_rule="one_success")  # läuft, sobald einer erfolgreich ist
    def teilergebnis():
        print("Mindestens eine Quelle ist da")

    vorgaenger = [stabil(), instabil()]
    vorgaenger >> nur_bei_erfolg()
    vorgaenger >> aufraeumen()
    vorgaenger >> alarm()
    vorgaenger >> teilergebnis()


trigger_rules()
