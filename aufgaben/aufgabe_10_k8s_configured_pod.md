# Aufgabe 10: Pod mit Env Vars und Ressourcen

*Tag 1, Kapitel: 05 Kubernetes Integration*

**Datei:** `participants/<dein-name>/k8s_configured_pod.py`

**Ziel:** Umgebungsvariablen und Ressourcen für einen Pod setzen.

## Task

* `image`: `python:3.11-slim`
* Umgebungsvariablen:
  * `ENV=prod`
  * `RUN_DATE={{ logical_date | ds }}`
* Ressourcen:
  * Requests: `250m` CPU, `256Mi` Speicher
  * Limits: `500m` CPU, `512Mi` Speicher
* Der Pod soll beide Variablen ausgeben

## Tipp

* Ressourcen über `container_resources=k8s.V1ResourceRequirements(requests=..., limits=...)`

---

**Musterlösung:** `musterloesungen/aufgabe_10_k8s_configured_pod.py`
