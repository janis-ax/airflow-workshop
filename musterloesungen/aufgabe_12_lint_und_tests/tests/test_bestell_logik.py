"""
Musterlösung Aufgabe 12: Unit-Tests für die Business-Logik aus Aufgabe 13.

Diese Tests brauchen kein laufendes Airflow, weil die Logik
in reinen Python-Funktionen steckt. Genau das ist der Vorteil.
"""

from __future__ import annotations

from musterloesungen.aufgabe_13_refactoring.bestell_logik import (
    erzeuge_bestellungen,
    filtere_gueltige,
    summiere_pro_land,
)


def test_erzeuge_bestellungen_anzahl():
    assert len(erzeuge_bestellungen(5, seed=1)) == 5


def test_filtere_gueltige_entfernt_null_und_negativ():
    daten = [{"amount": 10}, {"amount": 0}, {"amount": -5}]
    assert filtere_gueltige(daten) == [{"amount": 10}]


def test_summiere_pro_land():
    daten = [
        {"country": "DE", "amount": 10},
        {"country": "DE", "amount": 5},
        {"country": "FR", "amount": 20},
    ]
    assert summiere_pro_land(daten) == {"DE": 15, "FR": 20}
