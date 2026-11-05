"""
Musterlösung Aufgabe 9: Hello Pod in Kubernetes

Startet einen eigenen Pod mit alpine und gibt einen Text aus.
Die Logs des Pods erscheinen direkt im Task-Log (get_logs=True).

Hinweis: namespace und tolerations sind auf unsere Workshop-Umgebung
(OCI Kubernetes Cluster) abgestimmt. In anderen Clustern anpassen.
"""

from __future__ import annotations

import pendulum
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import DAG
from kubernetes.client import models as k8s

with DAG(
    dag_id="loesung_09_k8s_hello_pod",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["musterloesung", "aufgabe_09", "kubernetes"],
):
    KubernetesPodOperator(
        task_id="hello_pod",
        name="hello-pod",
        namespace="airflow-workshop",
        image="alpine:3.18",
        cmds=["/bin/sh", "-c"],
        arguments=['echo "Hello from Kubernetes Pod: {{ logical_date | ds }}" && sleep 5'],
        get_logs=True,
        on_finish_action="delete_pod",
        tolerations=[
            k8s.V1Toleration(
                key="oci.oraclecloud.com/oke-is-preemptible",
                operator="Exists",
                effect="NoSchedule",
            )
        ],
    )
