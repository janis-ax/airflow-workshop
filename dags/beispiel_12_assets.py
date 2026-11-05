"""
Beispiel 12: Assets (datengetriebenes Scheduling)

Statt nach Uhrzeit startet ein DAG, sobald ein anderer DAG Daten
aktualisiert hat. Producer schreibt das Asset (outlets),
Consumer hat das Asset als schedule.

Drei DAGs in dieser Datei:
- beispiel_12_producer:  klassisch mit outlets
- beispiel_12_consumer:  startet automatisch nach dem Producer
- beispiel_12_kundenstamm: der @asset Decorator erzeugt DAG, Task und Asset in einem
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, Asset, Metadata, asset, task

bestellungen = Asset("workshop_bestellungen")

# Producer: aktualisiert das Asset
with DAG(
    dag_id="beispiel_12_producer",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "assets"],
):

    @task(outlets=[bestellungen])
    def schreibe_bestellungen():
        print("Bestellungen geschrieben")
        # Metadaten an das Event hängen, der Consumer kann sie lesen
        yield Metadata(bestellungen, {"anzahl": 42})

    schreibe_bestellungen()

# Consumer: startet, sobald bestellungen aktualisiert wurde
with DAG(
    dag_id="beispiel_12_consumer",
    schedule=[bestellungen],
    catchup=False,
    tags=["beispiel", "assets"],
):

    @task
    def lies_event(triggering_asset_events=None):
        for asset_obj, events in (triggering_asset_events or {}).items():
            for event in events:
                print(f"{asset_obj.name}: {event.extra}")

    lies_event() >> BashOperator(task_id="weiterverarbeiten", bash_command='echo "Verarbeite"')


# @asset: Funktion = Asset + DAG + Task (alle heißen "beispiel_12_kundenstamm")
@asset(schedule="@daily", tags=["beispiel", "assets"])
def beispiel_12_kundenstamm():
    print("Kundenstamm aktualisiert")
