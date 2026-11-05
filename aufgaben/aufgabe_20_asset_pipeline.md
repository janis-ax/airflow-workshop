# Aufgabe 20: Asset-Aware Pipeline

*Tag 2, Kapitel: 13 Assets und Asset-Aware Scheduling*

**Datei:** `participants/<dein-name>/wetter_assets.py`

## Aufgabenstellung

Erstelle eine datengetriebene Pipeline mit drei Stufen:

1. Ein Producer lädt stündlich Wetterdaten und aktualisiert ein Asset
2. Eine Transformation berechnet Durchschnittswerte (Consumer des Wetter-Assets)
3. Ein Report erzeugt eine Zusammenfassung (Consumer der Durchschnittswerte)

## Anforderungen

* Den `@asset` Decorator nutzen
* Metadaten an die Events hängen (Anzahl Datenpunkte, Zeitraum)
* Der Report soll per `AssetOrTimeSchedule` auch täglich um 08:00 laufen
* Im Consumer die Event-Metadaten auslesen

## Bonus

* Logische Operatoren (`&`, `|`) für einen DAG, der auf mehrere Wetterstationen reagiert
* `AssetAlias` für dynamische Stationsnamen testen
* Ein Asset Event per REST API erzeugen

## Tipps

* Asset-Namen mit deinem Kürzel beginnen, damit sie eindeutig sind
* `from airflow.sdk import Metadata, asset`
* `from airflow.timetables.assets import AssetOrTimeSchedule`
* Siehe auch: `dags/beispiel_12_assets.py`

---

**Musterlösung:** `musterloesungen/aufgabe_20_assets_wetter_pipeline.py`
