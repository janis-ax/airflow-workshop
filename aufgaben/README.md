# Aufgaben

Alle Übungen aus dem Airflow-Seminar. Jede Aufgabe hat eine eigene Datei
und eine passende Musterlösung im Ordner [`../musterloesungen`](../musterloesungen).

## So arbeitest du

* Lege deine DAGs in deinem eigenen Ordner ab: `participants/<dein-name>/`
* Beginne jede `dag_id` mit deinem Kürzel, z. B. `ish_mein_erster_dag`.
  So kommen sich die DAGs der Teilnehmenden nicht in die Quere.
* Schreibe im Airflow-3-Stil: Imports aus `airflow.sdk` und aus
  `airflow.providers.standard...` (siehe Beispiele im Ordner [`../dags`](../dags))
* Schau erst in die Musterlösung, wenn du es selbst versucht hast

## Übersicht

| Nr. | Aufgabe | Tag | Kapitel |
|---|---|---|---|
| 1 | [Mein erster DAG](aufgabe_01_mein_erster_dag.md) | 1 | 02 DAG-Einführung |
| 2 | [DAG in der Oberfläche erkunden](aufgabe_02_dag_in_der_ui_erkunden.md) | 1 | 02 DAG-Einführung |
| 3 | [Scheduling und Catchup verstehen](aufgabe_03_scheduling_und_catchup.md) | 1 | 03 Scheduling und Orchestrierung |
| 4 | [Fan-In mit Trigger Rule](aufgabe_04_fan_in_trigger_rule.md) | 1 | 03 Scheduling und Orchestrierung |
| 5 | [Pool anlegen und nutzen](aufgabe_05_pool.md) | 1 | 03 Scheduling und Orchestrierung |
| 6 | [XCom Dataflow](aufgabe_06_xcom_dataflow.md) | 1 | 04 Datenaustausch |
| 7 | [Template Demo (Macros und Context)](aufgabe_07_template_demo.md) | 1 | 04 Datenaustausch |
| 8 | [Params, dag_run.conf, XCom und Templates](aufgabe_08_params_conf_xcom.md) | 1 | 04 Datenaustausch |
| 9 | [Hello Pod in Kubernetes](aufgabe_09_k8s_hello_pod.md) | 1 | 05 Kubernetes Integration |
| 10 | [Pod mit Env Vars und Ressourcen](aufgabe_10_k8s_configured_pod.md) | 1 | 05 Kubernetes Integration |
| 11 | [Failing Task analysieren](aufgabe_11_failing_task.md) | 1 | 06 Monitoring und Deployment |
| 12 | [Lint und Tests](aufgabe_12_lint_und_tests.md) | 2 | 07 CI/CD und Code-Qualität |
| 13 | [Anti-Pattern DAG refactoren](aufgabe_13_anti_pattern_refactoring.md) | 2 | 08 Best Practices und Anti-Patterns |
| 14 | [Konfiguration und Connections](aufgabe_14_config_und_connections.md) | 2 | 09 Secrets, Security und Konfiguration |
| 15 | [Sensor DAG](aufgabe_15_sensor.md) | 2 | 10 Skalierung, Langläufer und Sensoren |
| 16 | [Langläufer-Task optimieren](aufgabe_16_long_running.md) | 2 | 10 Skalierung, Langläufer und Sensoren |
| 17 | [Wiederholung: Wetter-Pipeline](aufgabe_17_wetter_pipeline.md) | 2 | Wiederholung |
| 18 | [Wiederholung: Parallele Datenverarbeitung](aufgabe_18_parallele_verarbeitung.md) | 2 | Wiederholung |
| 19 | [Human in the Loop: Content Review Workflow](aufgabe_19_hitl_content_review.md) | 2 | 12 Human in the Loop |
| 20 | [Asset-Aware Pipeline](aufgabe_20_asset_pipeline.md) | 2 | 13 Assets und Asset-Aware Scheduling |
| 21 | [Deferrable Sensor bauen und testen](aufgabe_21_deferrable_sensor.md) | 2 | 14 Deferrable Operators und Triggers |
| 22 | [Eigenen Trigger implementieren](aufgabe_22_custom_trigger.md) | 2 | 14 Deferrable Operators und Triggers |
| 23 | [Custom Timetable implementieren](aufgabe_23_custom_timetable.md) | 2 | 15 Timetables und Custom Scheduling |

## Vorlagen

Einige Aufgaben starten mit einem vorhandenen DAG, den du analysierst oder verbesserst.
Diese liegen in [`vorlagen/`](vorlagen):

| Datei | Für Aufgabe |
|---|---|
| `vorlage_11_failing_task.py` | 11: Failing Task analysieren |
| `vorlage_13_anti_pattern.py` | 13: Anti-Pattern DAG refactoren |
| `vorlage_16_long_running.py` | 16: Langläufer-Task optimieren |
