# Aufgabe 23: Custom Timetable implementieren

*Tag 2, Kapitel: 15 Timetables und Custom Scheduling*

## Aufgabe

Implementiere ein `EveryOtherSaturdayTimetable`, das jeden zweiten Samstag um 9 Uhr läuft.
Erstelle einen DAG, der dieses Timetable verwendet, und registriere es als Plugin.

1. Datei `custom_timetables.py` anlegen
2. `EveryOtherSaturdayTimetable` implementieren
3. `_next_even_saturday()` implementieren
4. `next_dagrun_info()` implementieren
5. `infer_manual_data_interval()` implementieren
6. `serialize()` und `deserialize()` implementieren
7. Als Plugin registrieren
8. Einen Test-DAG erstellen

## Hinweise

* Pendulum: `day_of_week` 5 = Samstag
* Epoch: ein bekannter Samstag, z. B. 2025-01-04
* Wochen seit der Epoch zählen: gerade Woche = Run, ungerade = überspringen
* Data Interval: 2 Wochen
* Zeitzone `Europe/Berlin` verwenden
* Die Datei gehört in den `plugins`-Ordner von Airflow, nicht in den DAG-Ordner

---

**Musterlösung:** `musterloesungen/aufgabe_23_custom_timetable/`
