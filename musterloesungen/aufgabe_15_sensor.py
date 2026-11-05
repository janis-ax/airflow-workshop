"""
Musterlösung Aufgabe 15: Sensor DAG

FileSensor im deferrable Modus: Während des Wartens belegt der Sensor
keinen Worker-Slot, der Triggerer übernimmt das Prüfen.

Hinweise:
- Der FileSensor nutzt die Connection "fs_default" (Typ File/Path).
  Falls sie fehlt: in der UI anlegen, Extra {"path": "/"}.
- Im deferrable Modus prüft der TRIGGERER, ob die Datei existiert.
  Die Datei muss also dort sichtbar sein.
- Den Pfad kann man beim Triggern über die Params ändern.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import DAG, Param

with DAG(
    dag_id="loesung_15_sensor",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    params={"datei": Param("/tmp/workshop/input.csv", type="string")},
    tags=["musterloesung", "aufgabe_15"],
):
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="{{ params.datei }}",
        poke_interval=60,
        timeout=1800,  # Sekunden, also 30 Minuten
        deferrable=True,
    )

    process_data = BashOperator(
        task_id="process_data",
        bash_command='echo "Datei {{ params.datei }} gefunden, Verarbeitung startet"',
    )

    wait_for_file >> process_data
