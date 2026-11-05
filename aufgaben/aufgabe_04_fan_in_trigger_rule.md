# Aufgabe 4: Fan-In mit Trigger Rule

*Tag 1, Kapitel: 03 Scheduling und Orchestrierung*

**Datei:** `participants/<dein-name>/orchestration_demo_dag.py`

**Struktur:** `A >> [B, C] >> D`

## Schritte

* Für Task D `trigger_rule="all_done"` setzen
* In Task B einen Fehler simulieren (`raise Exception(...)`)
* Beobachten: Läuft D trotzdem? Warum?

## Bonus

* D mit der Standardregel (`all_success`) laufen lassen und den Status vergleichen
* `one_failed` ausprobieren: Wofür könnte man das nutzen?

Siehe auch: `dags/beispiel_07_trigger_rules.py`

---

**Musterlösung:** `musterloesungen/aufgabe_04_fan_in_trigger_rule.py`
