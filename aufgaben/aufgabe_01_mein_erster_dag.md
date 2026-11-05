# Aufgabe 1: Mein erster DAG

*Tag 1, Kapitel: 02 DAG-Einführung*

**Datei:** `participants/<dein-name>/mein_erster_dag.py`

**Ziel:** Deinen ersten Airflow-3-DAG im Decorator-Stil schreiben.

## Anforderungen

* `dag_id`: `<dein-name>_mein_erster_dag`
* `start_date`: 2024-01-01, mit Zeitzone über `pendulum`
* `schedule`: `"@daily"`
* `catchup`: `False`

## Tasks

1. `start` (BashOperator): `echo "Start"`
2. `process` (`@task`): `print("Processing...")`
3. `end` (BashOperator): `echo "End"`

## Abhängigkeiten

```python
start >> process() >> end
```

## Tipps

* Imports in Airflow 3:
  ```python
  from airflow.sdk import dag, task
  from airflow.providers.standard.operators.bash import BashOperator
  ```
* Die DAG-Funktion am Ende der Datei einmal aufrufen, sonst findet Airflow den DAG nicht.
* Vorlage: `dags/beispiel_01_hallo_taskflow.py` und `dags/beispiel_02_klassisch_operatoren.py`

---

**Musterlösung:** `musterloesungen/aufgabe_01_mein_erster_dag.py`
