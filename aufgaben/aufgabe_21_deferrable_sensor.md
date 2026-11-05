# Aufgabe 21: Deferrable Sensor bauen und testen

*Tag 2, Kapitel: 14 Deferrable Operators und Triggers*

**Datei:** `participants/<dein-name>/deferrable_sensor_dag.py`

## Aufgabe

* Einen DAG mit einem FileSensor schreiben, der auf eine Datei wartet
* Der Sensor soll `deferrable=True` nutzen (intern mit dem eingebauten FileTrigger)
* Testen: Was passiert mit den Worker-Slots während der Wartezeit?

## Bonus

* Denselben Sensor zusätzlich mit `mode="poke"` und `mode="reschedule"` laufen lassen und die Slot-Nutzung vergleichen
* `start_from_trigger=True` ausprobieren

---

**Musterlösung:** `musterloesungen/aufgabe_21_deferrable_sensor.py`
