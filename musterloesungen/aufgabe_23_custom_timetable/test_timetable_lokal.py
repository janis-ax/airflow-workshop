"""
Schneller Test des Timetables ohne laufendes Airflow-Scheduling.

    cd musterloesungen/aufgabe_23_custom_timetable
    python test_timetable_lokal.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pendulum

sys.path.insert(0, str(Path(__file__).parent / "plugins"))

from airflow.timetables.base import TimeRestriction  # noqa: E402
from custom_timetables import EveryOtherSaturdayTimetable  # noqa: E402

tt = EveryOtherSaturdayTimetable()
restriction = TimeRestriction(
    earliest=pendulum.datetime(2025, 1, 1, tz="Europe/Berlin"), latest=None, catchup=True
)

letztes = None
for _ in range(5):
    info = tt.next_dagrun_info(last_automated_data_interval=letztes, restriction=restriction)
    print(
        f"Run {info.run_after}: {info.data_interval.start} bis {info.data_interval.end}"
    )
    letztes = info.data_interval
