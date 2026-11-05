"""
Musterlösung Aufgabe 14: Konfiguration und Connections

Voraussetzungen (in der UI anlegen):
- Variable   raw_data_path   z. B. /data/raw
- Connection my_example_db   z. B. Typ Postgres, Host db.example.local, Login workshop

Priorität für den Pfad:
1. dag_run.conf["raw_data_path"]   (pro Run, beim Triggern)
2. params["raw_data_path"]         (Standard im DAG, nur wenn gesetzt)
3. Variable "raw_data_path"        (zentral, für alle DAGs)
4. Fallback im Code

Die Connection wird gelesen, aber das Passwort wird NIE geloggt.
"""

from __future__ import annotations

import pendulum
from airflow.sdk import BaseHook, Param, Variable, dag, get_current_context, task

FALLBACK_PFAD = "/tmp/workshop/raw"


@dag(
    dag_id="loesung_14_config_und_connections",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    params={
        "raw_data_path": Param(
            None,
            type=["null", "string"],
            description="Optional: überschreibt die Variable raw_data_path",
        )
    },
    tags=["musterloesung", "aufgabe_14"],
)
def config_und_connections():
    @task
    def ermittle_pfad() -> str:
        context = get_current_context()
        conf = context["dag_run"].conf or {}

        if conf.get("raw_data_path"):
            pfad, quelle = conf["raw_data_path"], "dag_run.conf"
        elif context["params"].get("raw_data_path"):
            pfad, quelle = context["params"]["raw_data_path"], "params"
        else:
            # Variable wird erst HIER (im Task) gelesen, nicht auf Top-Level
            pfad = Variable.get("raw_data_path", default=None)
            quelle = "Variable"
            if pfad is None:
                pfad, quelle = FALLBACK_PFAD, "Fallback im Code"

        print(f"Pfad: {pfad} (Quelle: {quelle})")
        return pfad

    @task
    def zeige_connection():
        conn = BaseHook.get_connection("my_example_db")
        # Nur unkritische Felder loggen, niemals conn.password
        print(f"Connection-ID: {conn.conn_id}")
        print(f"Typ:           {conn.conn_type}")
        print(f"Host:          {conn.host}")
        print(f"Port:          {conn.port}")
        print(f"Schema:        {conn.schema}")
        print(f"Login:         {conn.login}")
        print(f"Passwort gesetzt: {'ja' if conn.password else 'nein'}")

    ermittle_pfad() >> zeige_connection()


config_und_connections()
