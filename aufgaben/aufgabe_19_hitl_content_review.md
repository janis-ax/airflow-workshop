# Aufgabe 19: Human in the Loop: Content Review Workflow

*Tag 2, Kapitel: 12 Human in the Loop*

**Datei:** `participants/<dein-name>/hitl_content_review.py`

**Voraussetzung:** Airflow 3.1 oder neuer.

## Aufgabenstellung

Erstelle einen Content Review Workflow mit folgenden Schritten:

1. `HITLEntryOperator`: Benutzer gibt einen Textentwurf und die Zielgruppe ein
2. Ein Task verarbeitet die Eingabe (z. B. Zusammenfassung erzeugen)
3. `ApprovalOperator`: Ein Reviewer genehmigt oder lehnt den Text ab
4. `HITLBranchOperator`: Bei Genehmigung wird veröffentlicht, sonst überarbeitet

## Anforderungen

* Jinja-Templates im `body` des ApprovalOperators, um die Eingabe anzuzeigen
* Timeout von 30 Minuten
* `assigned_users` für den Reviewer konfigurieren
* XCom, um Daten zwischen den Tasks weiterzugeben

## Bonus

* Eigenen Notifier schreiben, der eine Nachricht (z. B. Slack) sendet
* `generate_link_to_ui` für einen Direktlink nutzen
* Datenqualitäts-Check einbauen, der nur bei Anomalien manuell geprüft wird

## Tipps

* Import: `from airflow.providers.standard.operators.hitl import ApprovalOperator, HITLBranchOperator, HITLEntryOperator`
* Ergebnis des HITLEntryOperators im XCom: `{"params_input": {...}}`
* `assigned_users` braucht echte Airflow-Benutzer: `[{"id": "...", "name": "..."}]`

---

**Musterlösung:** `musterloesungen/aufgabe_19_hitl_content_review.py`
