# Aufgabe 7: Template Demo (Macros und Context)

*Tag 1, Kapitel: 04 Datenaustausch*

**Datei:** `participants/<dein-name>/template_demo_dag.py`

**Ziel:** Jinja-Templates und Macros nutzen.

## Task (BashOperator)

```bash
echo "Processing date {{ logical_date | ds }} ({{ data_interval_start }} - {{ data_interval_end }})"
```

## Schritte

* Deployen und triggern
* Logs prüfen
* In der UI beim Task "Rendered Template" anschauen
* Optional: mehrere Runs vergleichen

## Bonus

* `{{ macros.ds_add(ds, -1) }}` ausgeben: Was liefert das?

---

**Musterlösung:** `musterloesungen/aufgabe_07_template_demo.py`
