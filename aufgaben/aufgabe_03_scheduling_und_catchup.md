# Aufgabe 3: Scheduling und Catchup verstehen

*Tag 1, Kapitel: 03 Scheduling und Orchestrierung*

**Datei:** `participants/<dein-name>/schedule_demo_dag.py`

## Teilaufgabe 1: schedule-Presets

* `schedule="@hourly"`, `start_date` = 7 Tage in der Vergangenheit, `catchup=False`
* DAG aktivieren. Wie viele Runs werden erzeugt?

## Teilaufgabe 2: catchup=True

* `catchup` auf `True` setzen und den DAG neu aktivieren
* Im Grid beobachten: Wie viele historische Runs werden nachgeholt?

## Teilaufgabe 3: Cron-Ausdruck

* `schedule="30 9 * * 1-5"` (werktags um 09:30)
* Tipp: https://crontab.guru zum Testen

## Bonus

* `max_active_runs` setzen: Was ändert sich beim Nachholen?

---

**Musterlösung:** `musterloesungen/aufgabe_03_scheduling_und_catchup.py`
