"""
Business-Logik für die Bestell-Pipeline (Musterlösung Aufgabe 13).

Reine Python-Funktionen ohne Airflow-Abhängigkeit:
- lassen sich mit pytest testen
- werden im DAG nur noch aufgerufen
"""

from __future__ import annotations

import logging
import random

logger = logging.getLogger(__name__)


def erzeuge_bestellungen(anzahl: int, seed: int | None = None) -> list[dict]:
    """Erzeugt Beispiel-Bestellungen (statt einer echten Quelle)."""
    zufall = random.Random(seed)
    return [
        {
            "id": i,
            "country": zufall.choice(["DE", "FR", "ES"]),
            "amount": zufall.choice([10, 20, 0, -5, 50]),
        }
        for i in range(1, anzahl + 1)
    ]


def filtere_gueltige(bestellungen: list[dict]) -> list[dict]:
    """Behält nur Bestellungen mit positivem Betrag."""
    gueltig = [b for b in bestellungen if b["amount"] > 0]
    logger.info("%d von %d Bestellungen sind gültig", len(gueltig), len(bestellungen))
    return gueltig


def summiere_pro_land(bestellungen: list[dict]) -> dict[str, int]:
    """Summiert die Beträge pro Land."""
    summen: dict[str, int] = {}
    for b in bestellungen:
        summen[b["country"]] = summen.get(b["country"], 0) + b["amount"]
    return summen
