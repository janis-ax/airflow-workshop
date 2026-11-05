# Aufgabe 12: Lint und Tests

*Tag 2, Kapitel: 07 CI/CD und Code-Qualität*

**Ziel:** Linting und Tests lokal ausführen.

## Befehle

```bash
ruff check dags/ participants/
black --check dags/ participants/
isort --check-only dags/ participants/
pytest tests/
airflow dags test <dein-name>_mein_erster_dag 2024-01-01
```

## Aufgaben

* Eine `pyproject.toml` mit Einstellungen für ruff, black und isort anlegen
* Einen Test schreiben, der alle DAGs lädt und prüft, dass es keine Import-Fehler gibt
* Einen Test schreiben, der prüft, dass jeder DAG Tags hat
* Bonus: ruff mit den Airflow-Regeln (`AIR`) laufen lassen. Was findet er in alten Airflow-2-DAGs?

---

**Musterlösung:** `musterloesungen/aufgabe_12_lint_und_tests/`
