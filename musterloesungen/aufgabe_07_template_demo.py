"""
Musterlösung Aufgabe 7: Template Demo (Macros und Context)

Jinja-Templates werden erst zur Laufzeit gerendert.
Im Log sieht man die echten Werte des jeweiligen Runs.
Tipp: In der UI beim Task unter "Rendered Template" nachsehen.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="loesung_07_template_demo",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="@daily",
    catchup=False,
    tags=["musterloesung", "aufgabe_07"],
):
    BashOperator(
        task_id="zeige_templates",
        bash_command=(
            'echo "Processing date {{ logical_date | ds }} '
            '({{ data_interval_start }} - {{ data_interval_end }})"'
            # Ein paar weitere nützliche Werte zum Ausprobieren:
            ' && echo "DAG: {{ dag.dag_id }}, Run: {{ run_id }}"'
            ' && echo "Vortag: {{ macros.ds_add(ds, -1) }}"'
        ),
    )
