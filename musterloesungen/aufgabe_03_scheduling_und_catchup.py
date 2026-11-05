"""
Musterlösung Aufgabe 3: Scheduling und Catchup verstehen

Drei DAGs, einer pro Teilaufgabe. So lassen sie sich direkt nebeneinander
in der UI vergleichen.

ACHTUNG: Für die Übung nutzen wir ein start_date, das immer 7 Tage vor
"heute" liegt. In echten DAGs ist das ein Anti-Pattern: Dort gehört immer
ein festes Datum hin (siehe Best Practices).
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

# today() liefert Mitternacht, der Wert bleibt also einen Tag lang stabil.
SIEBEN_TAGE_ZURUECK = pendulum.today("UTC").subtract(days=7)

# Teilaufgabe 1: @hourly mit catchup=False
# Erwartung: Nach dem Aktivieren entsteht nur EIN Run (das letzte Intervall).
with DAG(
    dag_id="loesung_03a_hourly_ohne_catchup",
    start_date=SIEBEN_TAGE_ZURUECK,
    schedule="@hourly",
    catchup=False,
    tags=["musterloesung", "aufgabe_03"],
):
    BashOperator(
        task_id="zeige_datum",
        bash_command='echo "Intervall: {{ data_interval_start }} bis {{ data_interval_end }}"',
    )

# Teilaufgabe 2: @hourly mit catchup=True
# Erwartung: Airflow holt alle Stunden seit start_date nach (bis zu 168 Runs).
# max_active_runs begrenzt, wie viele davon gleichzeitig laufen.
with DAG(
    dag_id="loesung_03b_hourly_mit_catchup",
    start_date=SIEBEN_TAGE_ZURUECK,
    schedule="@hourly",
    catchup=True,
    max_active_runs=5,
    tags=["musterloesung", "aufgabe_03"],
):
    BashOperator(
        task_id="zeige_datum",
        bash_command='echo "Nachgeholter Run für {{ data_interval_start }}"',
    )

# Teilaufgabe 3: Cron-Ausdruck, werktags (Mo bis Fr) um 09:30
with DAG(
    dag_id="loesung_03c_cron_werktags",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="30 9 * * 1-5",
    catchup=False,
    tags=["musterloesung", "aufgabe_03"],
):
    BashOperator(
        task_id="zeige_datum",
        bash_command='echo "Werktags-Run: {{ logical_date | ds }}"',
    )
