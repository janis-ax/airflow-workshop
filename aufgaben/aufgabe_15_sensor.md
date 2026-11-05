# Aufgabe 15: Sensor DAG

*Tag 2, Kapitel: 10 Skalierung, Langläufer und Sensoren*

**Datei:** `participants/<dein-name>/sensor_demo_dag.py`

**Ziel:** FileSensor (am besten deferrable) mit anschließender Verarbeitung.

## Tasks

* `wait_for_file` (FileSensor)
  * `poke_interval=60`
  * `timeout=1800`
  * `deferrable=True`
* `process_data` (BashOperator)

## Abhängigkeiten

```python
wait_for_file >> process_data
```

## Hinweise

* Der FileSensor braucht die Connection `fs_default` (Typ File/Path).
* Was passiert, wenn die Datei nie kommt?

---

**Musterlösung:** `musterloesungen/aufgabe_15_sensor.py`
