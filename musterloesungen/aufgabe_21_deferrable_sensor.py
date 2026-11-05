"""
Musterlösung Aufgabe 21: Deferrable Sensor bauen und testen

Drei Sensoren warten auf dieselbe Datei, jeweils in einem anderen Modus.
So lässt sich direkt vergleichen, was mit den Worker-Slots passiert:

- warte_poke        mode="poke":       belegt den Worker-Slot die ganze Zeit
- warte_reschedule  mode="reschedule": gibt den Slot zwischen den Prüfungen frei
- warte_deferrable  deferrable=True:   Task geht in den Status "deferred",
                                       der Triggerer prüft, kein Worker-Slot belegt

Beobachten:
- Grid: Status der Sensoren (running, up_for_reschedule, deferred)
- Admin > Pools: Wie viele Slots belegt default_pool?
- Browse > Triggers (bzw. Admin): Der Trigger des deferrable Sensors

Hinweise:
- FileSensor nutzt die Connection "fs_default" (Typ File/Path, Extra {"path": "/"}).
- Im deferrable Modus prüft der Triggerer das Dateisystem, im poke/reschedule
  Modus der Worker. Die Datei muss am jeweiligen Ort existieren.
- Datei anlegen, z. B. mit: touch /tmp/workshop/fertig.txt
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import DAG, Param

with DAG(
    dag_id="loesung_21_deferrable_sensor",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    params={"datei": Param("/tmp/workshop/fertig.txt", type="string")},
    tags=["musterloesung", "aufgabe_21", "deferrable"],
):
    gemeinsam = {
        "filepath": "{{ params.datei }}",
        "poke_interval": 30,
        "timeout": 600,
        "soft_fail": True,  # nach Timeout "skipped" statt "failed"
    }

    warte_poke = FileSensor(task_id="warte_poke", mode="poke", **gemeinsam)
    warte_reschedule = FileSensor(task_id="warte_reschedule", mode="reschedule", **gemeinsam)
    warte_deferrable = FileSensor(task_id="warte_deferrable", deferrable=True, **gemeinsam)

    fertig = EmptyOperator(task_id="fertig", trigger_rule="none_failed")

    [warte_poke, warte_reschedule, warte_deferrable] >> fertig
