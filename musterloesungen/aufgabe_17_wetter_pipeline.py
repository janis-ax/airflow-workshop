"""
Musterlösung Aufgabe 17: Wiederholung Wetter-Pipeline

Kombiniert: Scheduling (Cron), Params, XCom mit TaskFlow, Templates.
Testen: einmal ohne Conf triggern, einmal mit {"city": "Hamburg"}.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import Param, dag, get_current_context, task


@dag(
    dag_id="loesung_17_wetter_pipeline",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="0 8 * * *",
    catchup=False,
    params={"city": Param("Berlin", type="string")},
    tags=["musterloesung", "aufgabe_17"],
)
def wetter_pipeline():
    @task
    def fetch_temperature() -> dict:
        context = get_current_context()
        result = {
            "city": context["params"]["city"],
            "temp": 22.5,
            "date": str(context["data_interval_end"]),
        }
        print(f"Temperatur abgerufen: {result}")
        return result

    @task
    def check_temperature(wetter: dict) -> str:
        bewertung = "warm" if wetter["temp"] >= 20 else "kalt"
        print(f"{wetter['city']}: {wetter['temp']} Grad, also {bewertung}")
        return bewertung

    log_result = BashOperator(
        task_id="log_result",
        bash_command=(
            "echo \"{{ logical_date | ds }}: {{ ti.xcom_pull(task_ids='check_temperature') }}\""
        ),
    )

    check_temperature(fetch_temperature()) >> log_result


wetter_pipeline()
