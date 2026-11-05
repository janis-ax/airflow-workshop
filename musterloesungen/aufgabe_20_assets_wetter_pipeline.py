"""
Musterlösung Aufgabe 20: Asset-Aware Pipeline

Drei Stufen, jede ist ein eigener DAG (der @asset Decorator erzeugt
pro Funktion automatisch DAG, Task und Asset mit gleichem Namen):

1. loesung_20_wetter_rohdaten     stündlich, erzeugt Messwerte + Metadaten
2. loesung_20_wetter_durchschnitt läuft, sobald loesung_20_wetter_rohdaten aktualisiert wurde
3. loesung_20_wetter_report       läuft nach loesung_20_wetter_durchschnitt ODER täglich um 08:00

Die Namen beginnen mit loesung_20_, damit sie nicht mit den
Assets der Teilnehmer kollidieren.

Die (kleinen) Daten reisen in den Metadaten der Asset Events.
So funktioniert die Übung auch mit dem KubernetesExecutor, wo Tasks
keine gemeinsame Festplatte haben. In echt würde man die Daten in
S3 oder eine Datenbank schreiben und nur Kennzahlen in die Metadaten legen.
"""

from __future__ import annotations

import random

import pendulum
from airflow.sdk import Metadata, asset
from airflow.timetables.assets import AssetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable


# 1) Producer: stündlich neue Wetterdaten
@asset(schedule="@hourly", tags=["musterloesung", "aufgabe_20"])
def loesung_20_wetter_rohdaten(self):
    temperaturen = [round(random.uniform(5, 25), 1) for _ in range(12)]
    jetzt = pendulum.now("Europe/Berlin")
    print(f"{len(temperaturen)} Messwerte geladen: {temperaturen}")

    # Metadaten an das Asset Event hängen
    yield Metadata(
        self,
        {
            "anzahl_messwerte": len(temperaturen),
            "zeitraum_von": jetzt.subtract(hours=1).to_iso8601_string(),
            "zeitraum_bis": jetzt.to_iso8601_string(),
            "temperaturen": temperaturen,
        },
    )


# 2) Transformation: Consumer von loesung_20_wetter_rohdaten
#    Der Parametername loesung_20_wetter_rohdaten macht das Asset automatisch zum Inlet.
@asset(schedule=[loesung_20_wetter_rohdaten], tags=["musterloesung", "aufgabe_20"])
def loesung_20_wetter_durchschnitt(self, context, loesung_20_wetter_rohdaten):
    events = context["inlet_events"][loesung_20_wetter_rohdaten]
    letztes = events[-1].extra
    werte = letztes["temperaturen"]
    durchschnitt = round(sum(werte) / len(werte), 2)

    print(
        f"Event-Metadaten: {letztes['anzahl_messwerte']} Werte "
        f"von {letztes['zeitraum_von']} bis {letztes['zeitraum_bis']}"
    )
    print(f"Durchschnitt: {durchschnitt} Grad")

    yield Metadata(
        self,
        {"durchschnitt": durchschnitt, "anzahl_messwerte": letztes["anzahl_messwerte"]},
    )


# 3) Report: läuft nach jeder neuen Berechnung ODER spätestens täglich um 08:00
@asset(
    schedule=AssetOrTimeSchedule(
        timetable=CronTriggerTimetable("0 8 * * *", timezone="Europe/Berlin"),
        assets=[loesung_20_wetter_durchschnitt],
    ),
    tags=["musterloesung", "aufgabe_20"],
)
def loesung_20_wetter_report(context, loesung_20_wetter_durchschnitt):
    events = context["inlet_events"][loesung_20_wetter_durchschnitt]
    if not events:
        print("Noch keine Durchschnittswerte vorhanden")
        return
    letztes = events[-1].extra
    print(
        f"Wetter-Report: Durchschnitt {letztes['durchschnitt']} Grad "
        f"aus {letztes['anzahl_messwerte']} Messwerten"
    )
