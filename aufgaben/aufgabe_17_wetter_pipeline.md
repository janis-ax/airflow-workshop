# Aufgabe 17: Wiederholung: Wetter-Pipeline

*Tag 2, Kapitel: Wiederholung*

**Datei:** `participants/<dein-name>/wetter_pipeline_dag.py`

**Ziel:** DAG-Grundlagen, Scheduling, XCom und Templates in einer einfachen Pipeline kombinieren.

## DAG

* `dag_id`: `<dein-name>_wetter_pipeline`
* `schedule`: `"0 8 * * *"` (täglich um 08:00)
* `start_date`: 2024-01-01
* `catchup`: `False`
* `params`: `{"city": "Berlin"}`

## Tasks

* `fetch_temperature` (`@task`): gibt `{"city": <params.city>, "temp": 22.5, "date": str(data_interval_end)}` zurück
* `check_temperature` (`@task`): bekommt das Dict, gibt `"warm"` zurück wenn `temp >= 20`, sonst `"kalt"`
* `log_result` (BashOperator):
  ```bash
  echo "{{ logical_date | ds }}: {{ ti.xcom_pull(task_ids='check_temperature') }}"
  ```

## Abhängigkeiten

```python
check_temperature(fetch_temperature()) >> log_result
```

## Schritte

1. DAG deployen und manuell triggern
2. XCom-Werte in der UI prüfen
3. Nochmal triggern mit Conf `{"city": "Hamburg"}`
4. Logs beider Runs vergleichen

---

**Musterlösung:** `musterloesungen/aufgabe_17_wetter_pipeline.py`
