# Aufgabe 13: Anti-Pattern DAG refactoren

*Tag 2, Kapitel: 08 Best Practices und Anti-Patterns*

**Vorlage:** `aufgaben/vorlagen/vorlage_13_anti_pattern.py`

## Analysepunkte

* Business-Logik im DAG
* Inkonsistentes Naming
* Große XComs
* Hartcodierte Pfade und Secrets
* Zu komplexer Single-Task-Monolith
* Gefährliche DAG-Einstellungen

## Ergebnis

* Liste der Probleme mit Begründung
* Refactoring: z. B. drei Tasks (extract, transform, load), Logik in einem eigenen Modul, Params statt fester Werte, Connection-ID statt Passwort im Code

## Bonus

* Unit-Tests für die ausgelagerte Logik schreiben (siehe Aufgabe 12)

---

**Musterlösung:** `musterloesungen/aufgabe_13_refactoring/`
