"""
Musterlösung Aufgabe 23: EveryOtherSaturdayTimetable

Läuft jeden zweiten Samstag um 09:00 (Europe/Berlin).
Data Interval: die zwei Wochen vor dem Run.

Diese Datei gehört in den plugins-Ordner von Airflow
(Scheduler, DAG-Prozessor und API-Server brauchen sie).
"""

from __future__ import annotations

import pendulum
from airflow.plugins_manager import AirflowPlugin
from airflow.timetables.base import DagRunInfo, DataInterval, Timetable
from pendulum import DateTime

SAMSTAG = 5  # pendulum: Montag = 0 ... Samstag = 5


class EveryOtherSaturdayTimetable(Timetable):
    """Jeden zweiten Samstag um 09:00."""

    def __init__(self, epoch_saturday: str = "2025-01-04", tz: str = "Europe/Berlin"):
        self._epoch_str = epoch_saturday
        self._tz_str = tz
        self._tz = pendulum.timezone(tz)
        self._epoch = pendulum.parse(epoch_saturday, tz=tz)
        self.description = f"Jeden zweiten Samstag um 09:00 ({tz})"

    @property
    def summary(self) -> str:
        return "Jeden 2. Samstag, 09:00"

    def _next_even_saturday(self, after: DateTime, inclusive: bool) -> DateTime:
        """Nächster 'gerader' Samstag 09:00 ab after (inclusive: after selbst zählt mit)."""
        lokal = after.in_timezone(self._tz)
        tage_bis_samstag = (SAMSTAG - lokal.day_of_week) % 7
        kandidat = lokal.add(days=tage_bis_samstag).set(hour=9, minute=0, second=0, microsecond=0)

        if kandidat < lokal or (kandidat == lokal and not inclusive):
            kandidat = kandidat.add(weeks=1)

        # Gerade Woche seit der Epoch: Run. Ungerade Woche: eine Woche weiter.
        wochen = (kandidat.date() - self._epoch.date()).days // 7
        if wochen % 2 != 0:
            kandidat = kandidat.add(weeks=1)
        return kandidat

    def next_dagrun_info(self, *, last_automated_data_interval, restriction):
        if last_automated_data_interval is not None:
            # Nach dem letzten Run: strikt danach suchen
            naechster = self._next_even_saturday(last_automated_data_interval.end, inclusive=False)
        else:
            if restriction.earliest is None:
                return None  # kein start_date
            start = restriction.earliest
            if not restriction.catchup:
                # Ohne catchup nicht in der Vergangenheit anfangen
                start = max(start, pendulum.now("UTC"))
            naechster = self._next_even_saturday(start, inclusive=True)

        if restriction.latest is not None and naechster > restriction.latest:
            return None  # end_date erreicht

        # Run um 09:00 am Samstag, Data Interval = die zwei Wochen davor
        return DagRunInfo.interval(start=naechster.subtract(weeks=2), end=naechster)

    def infer_manual_data_interval(self, *, run_after: DateTime) -> DataInterval:
        # Manueller Trigger: die zwei Wochen bis zum letzten geraden Samstag
        ende = self._next_even_saturday(run_after, inclusive=True)
        if ende > run_after:
            ende = ende.subtract(weeks=2)
        return DataInterval(start=ende.subtract(weeks=2), end=ende)

    def serialize(self) -> dict:
        return {"epoch_saturday": self._epoch_str, "tz": self._tz_str}

    @classmethod
    def deserialize(cls, data: dict) -> EveryOtherSaturdayTimetable:
        return cls(epoch_saturday=data["epoch_saturday"], tz=data["tz"])


class WorkshopTimetablePlugin(AirflowPlugin):
    name = "workshop_timetable_plugin"
    timetables = [EveryOtherSaturdayTimetable]
