# Aufgabe 6: XCom Dataflow

*Tag 1, Kapitel: 04 Datenaustausch*

**Datei:** `participants/<dein-name>/xcom_demo_dag.py`

**Ziel:** Daten zwischen Tasks weitergeben, in Airflow 3 am besten über TaskFlow.

## Tasks

* `produce_data` (`@task`): `return {"user": "ish", "score": 42}`
* `consume_data` (`@task`): bekommt das Dict als Parameter und gibt `"User <user> hat Score <score>"` aus
* `log_date` (BashOperator): `echo "Run {{ logical_date | ds }}"`

## Abhängigkeiten

```python
consume_data(produce_data()) >> log_date
```

## Bonus

* Den XCom-Wert in der UI finden (Task anklicken, Reiter XCom)

Siehe auch: `dags/beispiel_04_xcom_daten_weitergeben.py`

---

**Musterlösung:** `musterloesungen/aufgabe_06_xcom_dataflow.py`
