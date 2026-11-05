"""
Beispiel 14: Variablen und Connections richtig nutzen

Regeln:
- Variable.get() und Connections NUR innerhalb von Tasks lesen,
  nie auf Top-Level (wird sonst bei jedem Parsen ausgeführt)
- Passwörter niemals loggen
- In Templates: {{ var.value.name }} und {{ conn.conn_id.host }}

Zum Ausprobieren in der UI anlegen:
- Variable   workshop_umgebung = dev
- Connection workshop_api       Typ HTTP, Host api.example.com
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import BaseHook, Variable, dag, task


@dag(
    dag_id="beispiel_14_variablen_und_connections",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "konfiguration"],
)
def variablen_und_connections():
    @task
    def lies_variable() -> str:
        umgebung = Variable.get("workshop_umgebung", default="dev")
        print(f"Umgebung: {umgebung}")
        return umgebung

    @task
    def lies_connection():
        conn = BaseHook.get_connection("workshop_api")
        print(f"Host: {conn.host}, Login: {conn.login}")
        print(f"Passwort gesetzt: {'ja' if conn.password else 'nein'}")  # nie den Wert!

    template = BashOperator(
        task_id="per_template",
        bash_command=(
            "echo \"Umgebung: {{ var.value.get('workshop_umgebung', 'dev') }}\" && "
            'echo "API-Host: {{ conn.workshop_api.host }}"'
        ),
    )

    lies_variable() >> lies_connection() >> template


variablen_und_connections()
