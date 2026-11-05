"""
Musterlösung Aufgabe 22: Eigener Trigger (HttpStatusTrigger)

Der Trigger fragt eine URL periodisch ab und feuert ein TriggerEvent,
sobald der erwartete HTTP-Statuscode zurückkommt (oder der Timeout erreicht ist).

Wichtig: Der Triggerer muss diese Klasse importieren können.
Der Pfad in serialize() muss deshalb exakt zum Modulpfad passen.
"""

from __future__ import annotations

import asyncio
import time
import urllib.error
import urllib.request
from typing import Any

from airflow.exceptions import AirflowException
from airflow.sdk import BaseOperator
from airflow.triggers.base import BaseTrigger, TriggerEvent

TRIGGER_PFAD = "musterloesungen.aufgabe_22_custom_trigger.http_status_trigger.HttpStatusTrigger"


class HttpStatusTrigger(BaseTrigger):
    def __init__(
        self,
        url: str,
        expected_status_code: int = 200,
        poke_interval: float = 30.0,
        timeout: float | None = None,
    ):
        super().__init__()
        self.url = url
        self.expected_status_code = expected_status_code
        self.poke_interval = poke_interval
        self.timeout = timeout

    def serialize(self) -> tuple[str, dict[str, Any]]:
        # Klassenpfad + alle Argumente, mit denen der Triggerer den Trigger neu baut
        return (
            TRIGGER_PFAD,
            {
                "url": self.url,
                "expected_status_code": self.expected_status_code,
                "poke_interval": self.poke_interval,
                "timeout": self.timeout,
            },
        )

    def _hole_status(self) -> int | None:
        """Blockierender HTTP-Aufruf, läuft in einem eigenen Thread."""
        try:
            with urllib.request.urlopen(self.url, timeout=10) as antwort:
                return antwort.status
        except urllib.error.HTTPError as fehler:
            return fehler.code
        except Exception as fehler:  # Netzwerkfehler: einfach weiter warten
            self.log.warning("Abfrage von %s fehlgeschlagen: %s", self.url, fehler)
            return None

    async def run(self):
        start = time.monotonic()
        while True:
            # Bonus-Variante: hier aiohttp nutzen, dann braucht es keinen Thread
            status = await asyncio.to_thread(self._hole_status)
            self.log.info("%s antwortet mit Status %s", self.url, status)

            if status == self.expected_status_code:
                yield TriggerEvent({"status": "success", "status_code": status, "url": self.url})
                return

            if self.timeout is not None and time.monotonic() - start > self.timeout:
                yield TriggerEvent({"status": "timeout", "status_code": status, "url": self.url})
                return

            # Wichtig: asyncio.sleep statt time.sleep, sonst blockiert der ganze Triggerer
            await asyncio.sleep(self.poke_interval)


class WaitForHttpStatusOperator(BaseOperator):
    """Operator, der sich sofort an den HttpStatusTrigger übergibt (deferred)."""

    template_fields = ("url",)

    def __init__(
        self,
        url: str,
        expected_status_code: int = 200,
        poke_interval: float = 30.0,
        wait_timeout: float | None = 600,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.url = url
        self.expected_status_code = expected_status_code
        self.poke_interval = poke_interval
        self.wait_timeout = wait_timeout

    def execute(self, context):
        self.defer(
            trigger=HttpStatusTrigger(
                url=self.url,
                expected_status_code=self.expected_status_code,
                poke_interval=self.poke_interval,
                timeout=self.wait_timeout,
            ),
            method_name="execute_complete",
        )

    def execute_complete(self, context, event: dict[str, Any] | None = None):
        if not event or event["status"] != "success":
            raise AirflowException(f"Erwarteter Status nicht erreicht: {event}")
        self.log.info("%s liefert Status %s", event["url"], event["status_code"])
        return event["status_code"]
