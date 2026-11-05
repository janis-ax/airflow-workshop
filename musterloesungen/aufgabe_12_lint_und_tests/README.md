# Musterlösung Aufgabe 12: Lint und Tests

## Werkzeuge installieren

```bash
pip install ruff black isort pytest "apache-airflow>=3.1"
```

## Befehle (im Wurzelverzeichnis des Repos)

```bash
# Linting: findet Fehler, ungenutzte Imports und veraltete Airflow-2-Muster (Regeln AIR)
ruff check dags/ musterloesungen/

# Formatierung prüfen (ohne zu ändern)
black --check dags/ musterloesungen/
isort --check-only dags/ musterloesungen/

# Automatisch korrigieren
ruff check --fix dags/ musterloesungen/
black dags/ musterloesungen/
isort dags/ musterloesungen/

# Tests
pytest musterloesungen/aufgabe_12_lint_und_tests/tests/

# Einen DAG einmal komplett lokal durchlaufen lassen
airflow dags test loesung_01_mein_erster_dag 2024-01-01
```

## Dateien in diesem Ordner

| Datei | Inhalt |
|---|---|
| `pyproject.toml` | Konfiguration für ruff, black, isort und pytest |
| `tests/test_dag_integrity.py` | Lädt alle DAGs und prüft Import-Fehler, Tags und catchup |
| `tests/test_bestell_logik.py` | Unit-Tests für die Business-Logik aus Aufgabe 13 |

## Typische Funde von ruff

- `AIR` Regeln: alte Imports wie `from airflow.operators.bash import BashOperator`
  oder `schedule_interval`, die in Airflow 3 nicht mehr funktionieren
- `F401`: importiert, aber nicht benutzt
- `I001`: Imports nicht sortiert
