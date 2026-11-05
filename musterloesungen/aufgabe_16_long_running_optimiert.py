"""
Musterlösung Aufgabe 16: Langläufer-Task optimieren

Teil 1 (Analyse): aufgaben/vorlagen/vorlage_16_long_running.py
Ein einzelner Task schläft 10 Minuten. Probleme:
- blockiert einen Worker-Slot die ganze Zeit
- kein Timeout: hängt er, merkt es niemand
- bei Fehler muss alles von vorne laufen

Teil 2 (diese Lösung):
- Arbeit in drei Chunks aufgeteilt, die parallel laufen
- execution_timeout pro Chunk: hängt einer, wird er nach 5 Minuten abgebrochen
- schlägt ein Chunk fehl, wird nur dieser wiederholt
"""

from __future__ import annotations

from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG

with DAG(
    dag_id="loesung_16_long_running_optimiert",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    default_args={
        "execution_timeout": timedelta(minutes=5),  # gilt für jeden Task
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["musterloesung", "aufgabe_16"],
):
    start = EmptyOperator(task_id="start")
    finish = EmptyOperator(task_id="finish")

    chunks = [
        BashOperator(
            task_id=f"chunk_{i}",
            bash_command=f'echo "Chunk {i} startet" && sleep 120 && echo "Chunk {i} fertig"',
        )
        for i in range(1, 4)
    ]

    start >> chunks >> finish
