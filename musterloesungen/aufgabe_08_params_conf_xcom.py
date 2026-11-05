"""
Musterlösung Aufgabe 8: Params + dag_run.conf + XCom + Templates

Priorität beim Land:
1. dag_run.conf["country"] (beim Triggern mitgegeben)
2. params["country"] (Standardwert aus der DAG-Definition)

Testen:
- Trigger ohne Conf          -> DE
- Trigger mit {"country": "KR"} -> KR
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import Param, dag, get_current_context, task


@dag(
    dag_id="loesung_08_params_conf_xcom",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    params={"country": Param("DE", type="string", description="Ländercode")},
    tags=["musterloesung", "aufgabe_08"],
)
def params_conf_xcom():
    @task
    def read_country() -> str:
        context = get_current_context()
        conf = context["dag_run"].conf or {}
        country = conf.get("country") or context["params"]["country"]
        print(f"Verwende Land: {country}")
        return country

    build_path = BashOperator(
        task_id="build_path",
        bash_command=(
            'echo "/data/{{ logical_date | ds }}/'
            "{{ ti.xcom_pull(task_ids='read_country') }}/input.csv\""
        ),
    )

    final_log = BashOperator(
        task_id="final_log",
        bash_command="echo \"Done for {{ (dag_run.conf or {}).get('country', params.country) }}\"",
    )

    read_country() >> build_path >> final_log


params_conf_xcom()
