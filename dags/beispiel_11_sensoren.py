"""
Beispiel 11: Sensoren

Sensoren warten auf ein Ereignis. Drei Varianten:
1. @task.sensor: eigene Bedingung in Python (True = fertig)
2. TimeDeltaSensor deferrable: wartet eine Zeitspanne im Triggerer
3. FileSensor deferrable: wartet auf eine Datei

Modi:
- poke:        belegt den Worker-Slot die ganze Zeit (nur für kurze Wartezeiten)
- reschedule:  gibt den Slot zwischen den Prüfungen frei
- deferrable:  Triggerer übernimmt, kein Worker-Slot belegt (meist die beste Wahl)
"""

from __future__ import annotations

import random
from datetime import timedelta

import pendulum
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.providers.standard.sensors.time_delta import TimeDeltaSensor
from airflow.sdk import dag, task


@dag(
    dag_id="beispiel_11_sensoren",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "sensoren"],
)
def sensoren():
    # 1) Eigener Sensor: prüft alle 10 Sekunden, maximal 5 Minuten
    @task.sensor(poke_interval=10, timeout=300, mode="reschedule")
    def warte_auf_api() -> bool:
        bereit = random.random() < 0.3  # simuliert: API ist irgendwann bereit
        print(f"API bereit: {bereit}")
        return bereit

    # 2) Zeit abwarten, ohne einen Worker zu blockieren
    warte_30s = TimeDeltaSensor(
        task_id="warte_30_sekunden",
        delta=timedelta(seconds=30),
        deferrable=True,
    )

    # 3) Auf eine Datei warten. soft_fail: nach Timeout "skipped" statt "failed"
    #    Braucht die Connection fs_default (Typ File/Path).
    warte_datei = FileSensor(
        task_id="warte_auf_datei",
        filepath="/tmp/workshop/input.csv",
        poke_interval=30,
        timeout=120,
        soft_fail=True,
        deferrable=True,
    )

    @task(trigger_rule="none_failed")
    def weiter():
        print("Alle Bedingungen erfüllt (oder übersprungen)")

    [warte_auf_api(), warte_30s, warte_datei] >> weiter()


sensoren()
