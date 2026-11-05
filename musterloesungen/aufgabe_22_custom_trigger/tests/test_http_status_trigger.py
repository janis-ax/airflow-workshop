"""
Musterlösung Aufgabe 22 (Bonus): Test mit pytest-asyncio

    pip install pytest pytest-asyncio
    pytest musterloesungen/aufgabe_22_custom_trigger/tests/
"""

from __future__ import annotations

import pytest

from musterloesungen.aufgabe_22_custom_trigger.http_status_trigger import (
    TRIGGER_PFAD,
    HttpStatusTrigger,
)


def test_serialize():
    trigger = HttpStatusTrigger(url="https://example.com", expected_status_code=204)
    pfad, kwargs = trigger.serialize()
    assert pfad == TRIGGER_PFAD
    assert kwargs["expected_status_code"] == 204
    # Aus den serialisierten Daten muss sich der Trigger neu bauen lassen
    assert HttpStatusTrigger(**kwargs).url == "https://example.com"


@pytest.mark.asyncio
async def test_feuert_bei_erwartetem_status(monkeypatch):
    trigger = HttpStatusTrigger(url="https://example.com", poke_interval=0)
    monkeypatch.setattr(trigger, "_hole_status", lambda: 200)
    event = await trigger.run().__anext__()
    assert event.payload["status"] == "success"


@pytest.mark.asyncio
async def test_timeout(monkeypatch):
    trigger = HttpStatusTrigger(url="https://example.com", poke_interval=0, timeout=0)
    monkeypatch.setattr(trigger, "_hole_status", lambda: 503)
    event = await trigger.run().__anext__()
    assert event.payload["status"] == "timeout"
