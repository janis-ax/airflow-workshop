# Aufgabe 5: Pool anlegen und nutzen

*Tag 1, Kapitel: 03 Scheduling und Orchestrierung*

**Datei:** `participants/<dein-name>/pool_demo_dag.py`

## Schritte

* In der UI unter Admin > Pools einen Pool `<dein-name>_pool` mit 2 Slots anlegen
* Einen DAG mit drei parallelen Tasks schreiben, die je 30 Sekunden schlafen
* Allen drei Tasks den Pool zuweisen: `pool="<dein-name>_pool"`
* Im Grid beobachten: Laufen wirklich höchstens zwei Tasks gleichzeitig?

## Tipp

* Eine `@task`-Funktion mehrfach verwenden: `verarbeite.override(task_id="verarbeite_1")(1)`

---

**Musterlösung:** `musterloesungen/aufgabe_05_pool.py`
