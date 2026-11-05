# Beispiele

Kleine, lauffähige DAGs zum Nachschlagen. Jede Datei zeigt ein Thema und ist ausführlich kommentiert.
Alle starten nur manuell oder sind pausiert, man kann sie gefahrlos ausprobieren.

| Datei | Thema |
|---|---|
| `beispiel_01_hallo_taskflow.py` | Der kleinste DAG mit `@dag` und `@task` |
| `beispiel_02_klassisch_operatoren.py` | Klassischer Stil: `with DAG`, BashOperator, PythonOperator, EmptyOperator |
| `beispiel_03_abhaengigkeiten.py` | `>>`, Fan-Out, Fan-In und `chain()` |
| `beispiel_04_xcom_daten_weitergeben.py` | Daten weitergeben: `return`, `multiple_outputs`, `.output`, `xcom_pull` |
| `beispiel_05_templates_und_params.py` | Jinja-Templates, Macros und Params |
| `beispiel_06_branching.py` | `@task.branch` und `@task.short_circuit` |
| `beispiel_07_trigger_rules.py` | `all_done`, `one_failed`, `one_success` im Vergleich |
| `beispiel_08_retries_timeouts_callbacks.py` | Retries, Timeouts und Fehler-Callbacks |
| `beispiel_09_taskgroups.py` | TaskGroups (Ersatz für SubDAGs) |
| `beispiel_10_dynamic_task_mapping.py` | `expand()` und `partial()` |
| `beispiel_11_sensoren.py` | `@task.sensor`, TimeDeltaSensor und FileSensor (deferrable) |
| `beispiel_12_assets.py` | Producer, Consumer und der `@asset` Decorator |
| `beispiel_13_kubernetes_pod.py` | KubernetesPodOperator mit Env Vars und Ressourcen |
| `beispiel_14_variablen_und_connections.py` | Variablen und Connections sicher nutzen |
| `dummy_duck.py` | Rauchtest: Kommt der git-sync an? |
