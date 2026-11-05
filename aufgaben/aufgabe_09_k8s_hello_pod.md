# Aufgabe 9: Hello Pod in Kubernetes

*Tag 1, Kapitel: 05 Kubernetes Integration*

**Datei:** `participants/<dein-name>/k8s_hello_pod.py`

**Ziel:** Ein erster DAG mit dem KubernetesPodOperator.

## Task (KubernetesPodOperator)

* `image`: `alpine:3.18`
* `cmds`: `["/bin/sh", "-c"]`
* `arguments`:
  ```bash
  echo "Hello from Kubernetes Pod: {{ logical_date | ds }}" && sleep 5
  ```
* `namespace`: `airflow-workshop`
* `get_logs=True`

## Schritte

* Triggern, Logs prüfen
* Optional: mit `kubectl get pods -n airflow-workshop -w` zuschauen, wie der Pod entsteht und verschwindet

## Tipp

* Import: `from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator`
* Vorlage für tolerations: `dags/beispiel_13_kubernetes_pod.py`

---

**Musterlösung:** `musterloesungen/aufgabe_09_k8s_hello_pod.py`
