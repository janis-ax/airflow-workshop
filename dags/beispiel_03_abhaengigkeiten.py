"""
Beispiel 03: Abhängigkeiten, Fan-Out und Fan-In

    start >> [a, b, c] >> join >> ende

Außerdem: chain() für lange Ketten.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG, chain

with DAG(
    dag_id="beispiel_03_abhaengigkeiten",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "grundlagen", "abhaengigkeiten"],
):
    start = EmptyOperator(task_id="start")

    # Fan-Out: drei Tasks laufen parallel
    zweige = [
        BashOperator(task_id=f"zweig_{name}", bash_command=f'echo "Zweig {name}" && sleep 5')
        for name in ["a", "b", "c"]
    ]

    # Fan-In: join wartet auf alle drei
    join = EmptyOperator(task_id="join")

    schritt_1 = EmptyOperator(task_id="schritt_1")
    schritt_2 = EmptyOperator(task_id="schritt_2")
    ende = EmptyOperator(task_id="ende")

    start >> zweige >> join

    # chain() ist gleichbedeutend mit join >> schritt_1 >> schritt_2 >> ende
    chain(join, schritt_1, schritt_2, ende)
