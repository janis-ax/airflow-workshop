# Aufgabe 11: Failing Task analysieren

*Tag 1, Kapitel: 06 Monitoring und Deployment*

**Vorlage:** `aufgaben/vorlagen/vorlage_11_failing_task.py` (DAG `vorlage_11_failing_task`)

**Ziel:** Logs und Stacktrace lesen, Fehler beheben, erneut testen.

## Schritte

* Den Vorlage-DAG triggern und den Fehler ansehen
* Log und Stacktrace lesen: Welche Datei, welche Zeile, welche Meldung?
* Was passiert mit `inspect_context` und `log_run`? Warum?
* Den DAG in deinen Ordner kopieren, die Ursache beheben (dag_id anpassen!)
* Neu deployen und erneut testen

## Fragen

* Wie oft wurde der Task versucht? Wo sieht man das?
* Warum läuft `log_run` trotz Fehler?

---

**Musterlösung:** `musterloesungen/aufgabe_11_failing_task_gefixt.py`
