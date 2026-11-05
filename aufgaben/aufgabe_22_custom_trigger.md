# Aufgabe 22: Eigenen Trigger implementieren

*Tag 2, Kapitel: 14 Deferrable Operators und Triggers*

**Ordner:** `participants/<dein-name>/`

## Aufgabe: HttpStatusTrigger

* Erbt von `BaseTrigger`
* Parameter: `url`, `expected_status_code`, `poke_interval`
* Die `run()` Methode prüft periodisch den HTTP-Status
* Feuert ein `TriggerEvent`, wenn der erwartete Status eintritt
* Die `serialize()` Methode korrekt schreiben
* Einen Operator schreiben, der sich mit `self.defer(...)` an den Trigger übergibt, und ihn in einem DAG nutzen

## Bonus

* `aiohttp` für asynchrone HTTP-Requests nutzen
* Bei Timeout ein Fehler-Event senden
* Einen Test mit `pytest-asyncio` schreiben

## Tipps

* In `run()` niemals `time.sleep()` verwenden, sondern `await asyncio.sleep()`
* Der Pfad in `serialize()` muss der echte Modulpfad sein, sonst findet der Triggerer die Klasse nicht

---

**Musterlösung:** `musterloesungen/aufgabe_22_custom_trigger/`
