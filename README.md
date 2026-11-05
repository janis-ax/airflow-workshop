# airflow-workshop

DAGs, Aufgaben und Musterlösungen für das ORDIX Airflow-Seminar.
Das Repo wird per git-sync in die Workshop-Umgebung synchronisiert.
Alle Beispiele sind für **Airflow 3** geschrieben (HITL-Beispiele ab 3.1).

## Aufbau

```
airflow-workshop/
├── dags/              Klassische Einstiegsbeispiele zum Nachschlagen (dag_id: beispiel_...)
├── aufgaben/          Alle Übungen als Markdown, eine Datei pro Aufgabe
│   └── vorlagen/      Ausgangs-DAGs für einige Aufgaben (dag_id: vorlage_...)
├── musterloesungen/   Eine Lösung pro Aufgabe (dag_id: loesung_...)
└── participants/      Hier legt jede Person ihren eigenen Ordner an
```

## Für Teilnehmende

1. Eigenen Ordner anlegen: `participants/<dein-name>/`
2. Aufgaben stehen in [`aufgaben/README.md`](aufgaben/README.md)
3. Jede `dag_id` mit deinem Kürzel beginnen, z. B. `ish_mein_erster_dag`
4. Committen und pushen, nach kurzer Zeit erscheint der DAG in der Airflow-UI
5. Bei Fragen zur Syntax: erst in [`dags/`](dags) schauen, dann in die Musterlösung

## Airflow-3-Spickzettel

```python
import pendulum
from airflow.sdk import DAG, Param, dag, task            # DAG-Bausteine
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
```

* `schedule=` statt `schedule_interval=`
* `start_date` immer fest und mit Zeitzone: `pendulum.datetime(2024, 1, 1, tz="Europe/Berlin")`
* `catchup` ist standardmäßig `False`, ohne `schedule` läuft ein DAG nur manuell
* Im Kontext heißt es `logical_date` statt `execution_date`

## Hinweise für Trainer

* Alle DAGs in diesem Repo werden von Airflow geladen und sind beim Anlegen pausiert.
  Lösungen und Beispiele haben eindeutige Präfixe und kollidieren nicht mit den DAGs der Teilnehmenden.
* `.airflowignore` schließt Testdateien und die Timetable-Lösung (braucht ein Plugin) aus.
* Einige Lösungen brauchen Vorbereitung in der UI (Pools, Variablen, Connections).
  Das steht jeweils oben in der Datei.
* Imports wie `from musterloesungen....` funktionieren, weil Airflow die Repo-Wurzel
  als DAG-Ordner auf den Python-Pfad legt.
