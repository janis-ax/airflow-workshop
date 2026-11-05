"""
Musterlösung Aufgabe 13: Anti-Pattern DAG refactoren

Ausgangslage: aufgaben/vorlagen/vorlage_13_anti_pattern.py

Was wurde verbessert?
1. Business-Logik in eigenes Modul (bestell_logik.py), im DAG nur Aufrufe
2. Einheitliches Naming: snake_case, sprechende task_ids
3. Kleine XComs: nur Kennzahlen statt kompletter Daten und keine Secrets
4. Keine hardcodierten Pfade oder Passwörter: Params + Connection-ID
5. Monolith in drei Tasks zerlegt (extract, transform, load)
6. catchup=False, Retries und Timeout gesetzt, kein künstliches sleep

Hinweis zum Import: Airflow legt den DAG-Ordner (Repo-Wurzel) auf den
Python-Pfad. Deshalb funktioniert der Import über den Paketnamen.
"""

from __future__ import annotations

from datetime import timedelta

import pendulum
from airflow.sdk import Param, dag, task

from musterloesungen.aufgabe_13_refactoring.bestell_logik import (
    erzeuge_bestellungen,
    filtere_gueltige,
    summiere_pro_land,
)


@dag(
    dag_id="loesung_13_refactored_bestellungen",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={
        "owner": "data_team",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "execution_timeout": timedelta(minutes=10),
    },
    params={
        "anzahl": Param(10, type="integer", minimum=1),
        # Nur die ID der Connection, niemals Zugangsdaten im Code
        "ziel_conn_id": Param("my_example_db", type="string"),
    },
    tags=["musterloesung", "aufgabe_13"],
)
def refactored_bestellungen():
    @task
    def extract(params=None) -> list[dict]:
        return erzeuge_bestellungen(params["anzahl"])

    @task
    def transform(bestellungen: list[dict]) -> dict[str, int]:
        # Nur das kleine Ergebnis (Summen pro Land) geht als XCom weiter
        return summiere_pro_land(filtere_gueltige(bestellungen))

    @task
    def load(summen: dict[str, int], params=None):
        # In echt: Hook mit params["ziel_conn_id"] nutzen, z. B. PostgresHook
        print(f"Schreibe {len(summen)} Länder-Summen über Connection {params['ziel_conn_id']}")
        for land, summe in summen.items():
            print(f"  {land}: {summe}")

    load(transform(extract()))


refactored_bestellungen()
