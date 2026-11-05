# Aufgabe 16: Langläufer-Task optimieren

*Tag 2, Kapitel: 10 Skalierung, Langläufer und Sensoren*

**Vorlage:** `aufgaben/vorlagen/vorlage_16_long_running.py`

## Teil 1: Analyse

* `heavy_task` läuft sehr lange
* Auswirkungen in Grid und Gantt prüfen
* Welche Probleme entstehen dadurch?

## Teil 2: Optimierte Version

**Datei:** `participants/<dein-name>/long_running_optimized_dag.py`

* Tasks: `start`, `chunk_1`, `chunk_2`, `chunk_3` (z. B. `sleep 120`), `finish`
* `execution_timeout=timedelta(minutes=5)` pro Chunk

```python
start >> [chunk_1, chunk_2, chunk_3] >> finish
```

## Bonus

* Dynamic Task Mapping für beliebig viele Chunks (`expand()`)

---

**Musterlösung:** `musterloesungen/aufgabe_16_long_running_optimiert.py` und `musterloesungen/aufgabe_16_bonus_dynamic_mapping.py`
