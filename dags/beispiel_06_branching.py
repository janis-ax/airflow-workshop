"""
Beispiel 06: Verzweigungen mit @task.branch und @task.short_circuit

- @task.branch gibt die task_id zurück, mit der es weitergeht.
  Alle anderen direkten Nachfolger werden übersprungen (skipped).
- @task.short_circuit: gibt die Funktion False zurück, wird der Rest übersprungen.
- Ein Task NACH einer Verzweigung braucht eine passende Trigger Rule,
  sonst wird er mit übersprungen.
"""

from __future__ import annotations

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="beispiel_06_branching",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="@daily",
    catchup=False,
    tags=["beispiel", "branching"],
)
def branching():
    @task.short_circuit
    def ist_aktiv() -> bool:
        # z. B. Feature-Flag oder Feiertagsprüfung
        return True

    @task.branch
    def waehle_weg(logical_date=None) -> str:
        if logical_date.weekday() < 5:
            return "werktag"
        return "wochenende"

    @task
    def werktag():
        print("Volle Verarbeitung")

    @task
    def wochenende():
        print("Nur ein kleiner Report")

    @task(trigger_rule="none_failed_min_one_success")
    def abschluss():
        print("Fertig, egal welcher Weg gelaufen ist")

    ist_aktiv() >> waehle_weg() >> [werktag(), wochenende()] >> abschluss()


branching()
