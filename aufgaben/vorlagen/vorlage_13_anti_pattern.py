"""
ANTI-PATTERN DEMO DAG
=====================

Dieses Ding ist ABSICHTLICH schlecht gebaut.
Gedacht zum Zerlegen im Seminar / Vergleich mit best_practice_demo_dag.
"""

from __future__ import annotations

from datetime import timedelta
import json
import os
import random
import time
from typing import Any, Dict, List

import pendulum
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

# Hardcodierte "Config" & "DB-Connection" mitten im File (bitte NIE so machen)
RAW_FILE = "/tmp/anti_pattern/raw_data.json"
DB_CONN_STRING = "postgresql://user:supersecret@localhost:5432/prod_db"


def _do_everything(**kwargs) -> Dict[str, Any]:
    """
    Macht viel zu viel:
    - Daten generieren
    - Transformieren
    - "Laden"
    - nebenbei fette XCom zurückgeben
    """
    print("=== Task1: starting _do_everything ===")
    print(f"RAW_FILE (hardcoded path): {RAW_FILE}")
    print(f"Using DB connection string (!!!): {DB_CONN_STRING}")

    # "Extract": Fake-Daten direkt hier gebaut
    rows: List[Dict[str, Any]] = []
    for i in range(1, 11):
        rows.append(
            {
                "id": i,
                "country": random.choice(["DE", "FR", "ES"]),
                "amount": random.choice([10, 20, 0, -5, 50]),
            }
        )
    print(f"Generated {len(rows)} fake rows.")

    # "Transform": alles inline, kein Utils-Modul
    transformed: List[Dict[str, Any]] = []
    for row in rows:
        if row["amount"] <= 0:
            print(f"Skipping row {row['id']} because amount <= 0")
            continue
        row["processed_flag"] = True
        transformed.append(row)
    print(f"Kept {len(transformed)} rows after transform.")

    # "Load": einfach in eine Datei schreiben + Sleep simuliert „Langläufer“
    os.makedirs(os.path.dirname(RAW_FILE), exist_ok=True)
    with open(RAW_FILE, "w", encoding="utf-8") as f:
        json.dump(transformed, f)
    print(f"Wrote transformed data to {RAW_FILE}")

    print("Simulating heavy work with sleep(10)...")
    time.sleep(10)

    print("Pretending to insert into DB...")
    for t in transformed:
        print(f"[FAKE INSERT] {t}")

    # viel zu großer XCom: komplette Daten + Metadaten
    result = {
        "raw_file": RAW_FILE,
        "row_count": len(rows),
        "row_count_after_transform": len(transformed),
        "preview": transformed[:5],
        "db_conn_used": DB_CONN_STRING,
        "run_ts": kwargs.get("ts"),
    }
    print("=== Task1: finished, returning huge XCom ===")
    return result


def _follow_up(**kwargs) -> None:
    """
    Zieht unnötig den ganzen XCom wieder rein und macht fast nichts.
    """
    print("=== Task2: starting _follow_up ===")
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="Task1DoEverything")
    print("Got XCom from Task1DoEverything:")
    print(json.dumps(data, indent=2))
    print("No validation, no error handling. All good. 🙃")
    print("=== Task2: done ===")


with DAG(
    dag_id="vorlage_13_anti_pattern",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,         # im Original "@daily": hier aus, damit catchup nicht hunderte Runs erzeugt
    catchup=True,          # ABSICHTLICH schlecht: Backfills ohne Ende
    default_args={
        "owner": "data_team",
        "retries": 0,       # ABSICHTLICH schlecht: keine Retries
        "retry_delay": timedelta(minutes=5),
    },
    tags=["vorlage", "aufgabe_13", "anti_pattern"],
) as dag:
    task1 = PythonOperator(
        task_id="Task1DoEverything",  # unsauberer Name (absichtlich)
        python_callable=_do_everything,
    )

    task2 = PythonOperator(
        task_id="FINAL_task",         # inkonsistentes Naming (absichtlich)
        python_callable=_follow_up,
    )

    task1 >> task2
