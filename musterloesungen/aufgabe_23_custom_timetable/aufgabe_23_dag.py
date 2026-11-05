"""
Musterlösung Aufgabe 23: Test-DAG für das EveryOtherSaturdayTimetable

Voraussetzung: plugins/custom_timetables.py liegt im plugins-Ordner von Airflow
und Airflow wurde danach neu gestartet.

Diese Datei steht in .airflowignore, damit sie ohne installiertes Plugin
keinen Import-Fehler in der UI erzeugt. Zum Ausprobieren in den eigenen
DAG-Ordner kopieren.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG
from custom_timetables import EveryOtherSaturdayTimetable  # aus dem plugins-Ordner

with DAG(
    dag_id="loesung_23_jeden_zweiten_samstag",
    start_date=pendulum.datetime(2025, 1, 1, tz="Europe/Berlin"),
    schedule=EveryOtherSaturdayTimetable(epoch_saturday="2025-01-04"),
    catchup=False,
    tags=["musterloesung", "aufgabe_23", "timetable"],
):
    BashOperator(
        task_id="zweiwochen_report",
        bash_command='echo "Report für {{ data_interval_start }} bis {{ data_interval_end }}"',
    )
