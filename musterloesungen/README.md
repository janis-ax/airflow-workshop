# Musterlösungen

Eine lauffähige Lösung pro Aufgabe aus [`../aufgaben`](../aufgaben).
Alle dag_ids beginnen mit `loesung_`, damit sie nicht mit euren DAGs kollidieren.

| Nr. | Aufgabe | Lösung | Vorbereitung |
|---|---|---|---|
| 1 | Mein erster DAG | `aufgabe_01_mein_erster_dag.py` | |
| 2 | DAG in der UI erkunden | siehe unten | |
| 3 | Scheduling und Catchup | `aufgabe_03_scheduling_und_catchup.py` (drei DAGs) | |
| 4 | Fan-In mit Trigger Rule | `aufgabe_04_fan_in_trigger_rule.py` | |
| 5 | Pool | `aufgabe_05_pool.py` | Pool `workshop_pool` (2 Slots) |
| 6 | XCom Dataflow | `aufgabe_06_xcom_dataflow.py` | |
| 7 | Template Demo | `aufgabe_07_template_demo.py` | |
| 8 | Params, Conf, XCom, Templates | `aufgabe_08_params_conf_xcom.py` | |
| 9 | Hello Pod | `aufgabe_09_k8s_hello_pod.py` | Kubernetes-Provider |
| 10 | Pod mit Env Vars und Ressourcen | `aufgabe_10_k8s_configured_pod.py` | Kubernetes-Provider |
| 11 | Failing Task | `aufgabe_11_failing_task_gefixt.py` | |
| 12 | Lint und Tests | `aufgabe_12_lint_und_tests/` | ruff, black, isort, pytest |
| 13 | Anti-Pattern refactoren | `aufgabe_13_refactoring/` | |
| 14 | Konfiguration und Connections | `aufgabe_14_config_und_connections.py` | Variable `raw_data_path`, Connection `my_example_db` |
| 15 | Sensor DAG | `aufgabe_15_sensor.py` | Connection `fs_default` |
| 16 | Langläufer optimieren | `aufgabe_16_long_running_optimiert.py`, Bonus: `aufgabe_16_bonus_dynamic_mapping.py` | |
| 17 | Wetter-Pipeline | `aufgabe_17_wetter_pipeline.py` | |
| 18 | Parallele Verarbeitung | `aufgabe_18_parallele_verarbeitung.py` | Pool `verarbeitung_pool` (2 Slots) |
| 19 | Human in the Loop | `aufgabe_19_hitl_content_review.py` | Airflow 3.1+, Benutzer in `assigned_users` |
| 20 | Asset-Aware Pipeline | `aufgabe_20_assets_wetter_pipeline.py` | |
| 21 | Deferrable Sensor | `aufgabe_21_deferrable_sensor.py` | Triggerer, Connection `fs_default` |
| 22 | Eigener Trigger | `aufgabe_22_custom_trigger/` | Triggerer |
| 23 | Custom Timetable | `aufgabe_23_custom_timetable/` | Plugin installieren (siehe unten) |

## Lösung Aufgabe 2: DAG in der UI erkunden

* **Dauer von `process`:** im Grid auf den Task klicken, die Details zeigen Start, Ende und Dauer
  (bei einem `print` meist unter einer Sekunde, plus Startzeit des Workers).
* **Log von `process`:** enthält die Zeile `Processing...` zwischen den Airflow-Meldungen.
* **Nächster geplanter Run:** steht in der DAG-Übersicht ("Next Run"). Bei `@daily` ist das der nächste Tageswechsel.
* Ein manuell getriggerter Run hat eine `run_id`, die mit `manual__` beginnt, ein geplanter beginnt mit `scheduled__`.

## Lösung Aufgabe 13: Gefundene Anti-Patterns

| Problem in der Vorlage | Warum schlecht | Lösung |
|---|---|---|
| Alles in einem Task (`_do_everything`) | Kein Neustart einzelner Schritte, schwer zu testen | Drei Tasks: extract, transform, load |
| Logik direkt in der DAG-Datei | Nicht testbar ohne Airflow | Modul `bestell_logik.py` mit reinen Funktionen |
| `DB_CONN_STRING` mit Passwort im Code | Secret landet in Git und im Log | Nur Connection-ID als Param, Zugangsdaten in Airflow Connections |
| Hartcodierter Pfad `RAW_FILE` | Nicht konfigurierbar, im Pod oft nicht vorhanden | Params bzw. Variablen |
| Riesiger XCom inkl. Connection-String | Belastet die Metadaten-DB, verrät Secrets | Nur kleine Kennzahlen weitergeben |
| `Task1DoEverything`, `FINAL_task` | Uneinheitlich, nicht sprechend | snake_case, beschreibt die Aufgabe |
| `catchup=True` ab 2023, `retries=0` | Hunderte Backfill-Runs, kein Schutz vor Aussetzern | `catchup=False`, Retries und Timeout |
| `time.sleep(10)` | Blockiert Worker-Slot ohne Nutzen | Entfernt |

## Aufgabe 23: Timetable ausprobieren

Das Timetable muss als Plugin installiert sein, deshalb ist der Ordner in `.airflowignore` ausgeschlossen.

1. `aufgabe_23_custom_timetable/plugins/custom_timetables.py` in den `plugins`-Ordner von Airflow kopieren
2. Scheduler, DAG-Prozessor und API-Server neu starten
3. `aufgabe_23_dag.py` in den DAG-Ordner kopieren
4. Schnelltest ohne Scheduler: `python test_timetable_lokal.py`

## Tests

```bash
pip install pytest pytest-asyncio "apache-airflow>=3.1"
pytest musterloesungen/
```
