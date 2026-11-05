# Aufgabe 8: Params, dag_run.conf, XCom und Templates

*Tag 1, Kapitel: 04 Datenaustausch*

**Datei:** `participants/<dein-name>/data_exchange_demo_dag.py`

**Ziel:** Laufzeit-Parameter, XCom und Templates kombinieren.

## DAG

* `schedule=None`, `catchup=False`
* `params={"country": Param("DE", type="string")}`

## Tasks

* `read_country` (`@task`): liest zuerst `dag_run.conf["country"]`, sonst `params["country"]`, und gibt das Land zurück
* `build_path` (BashOperator):
  ```bash
  echo "/data/{{ logical_date | ds }}/{{ ti.xcom_pull(task_ids='read_country') }}/input.csv"
  ```
* `final_log` (BashOperator):
  ```bash
  echo "Done for {{ (dag_run.conf or {}).get('country', params.country) }}"
  ```

## Abhängigkeiten

```python
read_country() >> build_path >> final_log
```

## Schritte

* Run ohne Conf
* Run mit Conf `{"country": "KR"}`
* Logs vergleichen

## Tipp

* Den Kontext in einer `@task`-Funktion holen: `from airflow.sdk import get_current_context`

---

**Musterlösung:** `musterloesungen/aufgabe_08_params_conf_xcom.py`
