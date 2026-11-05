"""
Musterlösung Aufgabe 19: Human in the Loop, Content Review Workflow

Ablauf:
1. text_eingeben     (HITLEntryOperator)  Benutzer gibt Entwurf und Zielgruppe ein
2. fasse_zusammen    (@task)              erzeugt eine kurze Zusammenfassung
3. freigabe          (ApprovalOperator)   Reviewer genehmigt oder lehnt ab
4. naechster_schritt (HITLBranchOperator) veröffentlichen oder überarbeiten
5. veroeffentlichen / ueberarbeiten

Voraussetzung: Airflow 3.1 oder neuer (HITL-Operatoren im Standard-Provider).

WICHTIG: assigned_users muss zu echten Airflow-Benutzern passen.
"admin" ist ein Platzhalter. Steht dort ein Benutzer, den es nicht gibt,
kann niemand antworten.
"""

from __future__ import annotations

from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.hitl import (
    ApprovalOperator,
    HITLBranchOperator,
    HITLEntryOperator,
)
from airflow.sdk import Param, dag, task

REVIEWER = [{"id": "admin", "name": "Workshop Reviewer"}]
TIMEOUT = timedelta(minutes=30)


@dag(
    dag_id="loesung_19_hitl_content_review",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["musterloesung", "aufgabe_19", "hitl"],
)
def hitl_content_review():
    # 1) Eingabe sammeln: In der UI erscheint ein Formular
    text_eingeben = HITLEntryOperator(
        task_id="text_eingeben",
        subject="Bitte Textentwurf und Zielgruppe eingeben",
        params={
            "entwurf": Param("", type="string", description="Der Textentwurf"),
            "zielgruppe": Param(
                "Kunden",
                type="string",
                enum=["Kunden", "Mitarbeitende", "Presse"],
                description="Für wen ist der Text?",
            ),
        },
        execution_timeout=TIMEOUT,
    )

    # 2) Eingabe verarbeiten: Ergebnis des HITL-Tasks kommt per XCom
    @task
    def fasse_zusammen(eingabe: dict) -> dict:
        werte = eingabe["params_input"]
        entwurf = werte["entwurf"]
        zusammenfassung = entwurf[:100] + ("..." if len(entwurf) > 100 else "")
        return {
            "zielgruppe": werte["zielgruppe"],
            "woerter": len(entwurf.split()),
            "zusammenfassung": zusammenfassung,
        }

    zusammenfassung = fasse_zusammen(text_eingeben.output)

    # 3) Freigabe: body nutzt Jinja-Templates, um die Daten anzuzeigen
    freigabe = ApprovalOperator(
        task_id="freigabe",
        subject="Text zur Veröffentlichung freigeben?",
        body=(
            "Zielgruppe: {{ ti.xcom_pull(task_ids='fasse_zusammen')['zielgruppe'] }}\n"
            "Wörter: {{ ti.xcom_pull(task_ids='fasse_zusammen')['woerter'] }}\n"
            "Zusammenfassung: {{ ti.xcom_pull(task_ids='fasse_zusammen')['zusammenfassung'] }}"
        ),
        assigned_users=REVIEWER,
        defaults="Reject",  # ohne Antwort nach 30 Minuten: abgelehnt
        execution_timeout=TIMEOUT,
    )

    # 4) Verzweigung: Die Optionen sind die task_ids der nächsten Tasks
    naechster_schritt = HITLBranchOperator(
        task_id="naechster_schritt",
        subject="Wie geht es weiter?",
        options=["veroeffentlichen", "ueberarbeiten"],
        assigned_users=REVIEWER,
        execution_timeout=TIMEOUT,
    )

    @task
    def veroeffentlichen(info: dict):
        print(f"Text für {info['zielgruppe']} wird veröffentlicht")

    @task
    def ueberarbeiten(info: dict):
        print(f"Text für {info['zielgruppe']} geht zurück in die Überarbeitung")

    zusammenfassung >> freigabe >> naechster_schritt
    naechster_schritt >> [veroeffentlichen(zusammenfassung), ueberarbeiten(zusammenfassung)]


hitl_content_review()
