# Aufgabe 18: Wiederholung: Parallele Datenverarbeitung

*Tag 2, Kapitel: Wiederholung*

**Datei:** `participants/<dein-name>/parallel_processing_dag.py`

**Ziel:** Orchestrierung, Trigger Rules und Pools wiederholen.

**Voraussetzung:** Pool `<dein-name>_verarbeitung_pool` mit 2 Slots anlegen (Admin > Pools).

## Tasks

* `start` (EmptyOperator)
* `laden_csv`, `laden_json`, `laden_xml` (`@task`): geben "CSV/JSON/XML geladen" aus, alle im Pool
* `zusammenfuehren` (`@task`): `trigger_rule="all_done"`
* `report` (BashOperator): `echo "Report erstellt am {{ logical_date | ds }}"`

## Abhängigkeiten

```python
start >> [laden_csv, laden_json, laden_xml] >> zusammenfuehren >> report
```

## Schritte

1. DAG deployen und triggern
2. Im Grid prüfen: Laufen wirklich nur zwei Lade-Tasks gleichzeitig?
3. Einen Lade-Task absichtlich fehlschlagen lassen (`raise Exception`)
4. Beobachten: Läuft `zusammenfuehren` trotzdem? Warum?

Tipp: `EmptyOperator` kommt aus `airflow.providers.standard.operators.empty`.

---

**Musterlösung:** `musterloesungen/aufgabe_18_parallele_verarbeitung.py`
