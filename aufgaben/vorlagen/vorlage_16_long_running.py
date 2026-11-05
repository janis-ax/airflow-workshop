"""
VORLAGE Aufgabe 16: Langläufer-Task optimieren
Diesen DAG analysieren. Die Musterlösung liegt in musterloesungen/.
"""

from __future__ import annotations

import time

import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="vorlage_16_long_running",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    default_args={
        "owner": "data_team",
        "retries": 0,  # Anti-Pattern-Demo
    },
    tags=["vorlage", "aufgabe_16"],
)
def long_running_demo_dag():
    @task(task_id="heavy_task")
    def heavy_task() -> None:
        """
        Simuliert einen viel zu langen Task.
        Keine Timeouts, kein Chunking, blockiert einfach nur Worker-Ressourcen.
        """
        print("heavy_task: starting long-running job (sleep 600)...")
        time.sleep(600)  # 10 Minuten warten
        print("heavy_task: finished.")

    heavy_task()


long_running_demo_dag()
