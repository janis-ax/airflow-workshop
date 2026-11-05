"""
Musterlösung Aufgabe 12: DAG-Integritätstests

Prüft für alle DAGs im Repo:
- lassen sich ohne Import-Fehler laden
- haben Tags
- haben catchup=False (unsere Team-Regel)
- haben keine Zyklen (prüft Airflow beim Laden automatisch)

Ausführen im Repo-Wurzelverzeichnis:
    pytest musterloesungen/aufgabe_12_lint_und_tests/tests/
"""

from __future__ import annotations

from pathlib import Path

import pytest

try:  # Airflow 3.1+
    from airflow.dag_processing.dagbag import DagBag
except ImportError:  # ältere Versionen
    from airflow.models import DagBag

REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def dagbag() -> DagBag:
    return DagBag(dag_folder=str(REPO_ROOT), include_examples=False)


def test_keine_import_fehler(dagbag):
    assert dagbag.import_errors == {}, f"Import-Fehler: {dagbag.import_errors}"


def test_dags_vorhanden(dagbag):
    assert len(dagbag.dags) > 0


@pytest.mark.parametrize("pflicht", ["tags"])
def test_alle_dags_haben_tags(dagbag, pflicht):
    ohne = [dag_id for dag_id, dag in dagbag.dags.items() if not getattr(dag, pflicht)]
    assert not ohne, f"DAGs ohne {pflicht}: {ohne}"


def test_catchup_aus(dagbag):
    # Ausnahmen: Catchup-Demo aus Aufgabe 3 und die Anti-Pattern-Vorlage
    erlaubt = {"loesung_03b_hourly_mit_catchup", "vorlage_13_anti_pattern"}
    mit_catchup = [d for d, dag in dagbag.dags.items() if dag.catchup and d not in erlaubt]
    assert not mit_catchup, f"DAGs mit catchup=True: {mit_catchup}"
