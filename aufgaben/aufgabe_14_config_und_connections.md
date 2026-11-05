# Aufgabe 14: Konfiguration und Connections

*Tag 2, Kapitel: 09 Secrets, Security und Konfiguration*

**Datei:** `participants/<dein-name>/config_and_connection_demo_dag.py`

**Ziel:** `dag_run.conf`, `params`, `Variable` und `Connection` sauber priorisieren, ohne Secrets zu loggen.

## Voraussetzungen (in der UI anlegen)

* Variable `<dein-name>_raw_data_path`, z. B. `/data/raw`
* Connection `<dein-name>_example_db`, z. B. Typ Postgres mit Host, Login und Passwort

## Der Task soll loggen

* Den Pfad und woher er kommt (conf, params oder Variable)
* Die Connection-Details ohne Passwort

## Tipps

* `from airflow.sdk import BaseHook, Variable`
* Variablen und Connections nur INNERHALB von Tasks lesen

---

**Musterlösung:** `musterloesungen/aufgabe_14_config_und_connections.py`
