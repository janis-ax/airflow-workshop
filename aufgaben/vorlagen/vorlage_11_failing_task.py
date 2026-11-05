"""
VORLAGE Aufgabe 11: Failing Task analysieren
Diesen DAG analysieren. Die Musterlösung liegt in musterloesungen/.
"""

from __future__ import annotations

from datetime import timedelta

import pendulum
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator


@dag(
    dag_id="vorlage_11_failing_task",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    default_args={
        "owner": "data_team",
        "retries": 1,  # shows retries in the UI
        "retry_delay": timedelta(minutes=1),
    },
    tags=["vorlage", "aufgabe_11"],
)
def failing_task_demo_dag():
    @task(task_id="failing_task")
    def failing_task() -> None:
        """
        Absichtlicher Fehler:
        - wird jedes Mal mit Exception abbrechen
        - perfekt, um Logs / Retries / UI zu zeigen
        """
        # In Airflow 3, run_id is available via templates/context at runtime,
        # but we don't need it to demonstrate a failure.
        raise RuntimeError("Demo failure in failing_task_demo_dag (intentional)")

    @task(task_id="inspect_context")
    def inspect_context() -> None:
        """
        Läuft nur, wenn failing_task irgendwann gefixt wurde.
        """
        print("[inspect_context] DAG is now healthy")

    log_run = BashOperator(
        task_id="log_run",
        bash_command=(
            'echo "Run {{ run_id }} finished at {{ ts }} with state={{ ti.state }}"'
        ),
        trigger_rule="all_done",  # runs even if upstream failed
    )

    ft = failing_task()
    ic = inspect_context()

    ft >> ic
    [ft, ic] >> log_run


failing_task_demo_dag()
