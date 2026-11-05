"""
Beispiel 13: KubernetesPodOperator

Jeder Task läuft in einem eigenen Pod mit eigenem Image.
Ideal, wenn ein Task andere Bibliotheken, eine andere Sprache
oder viel Speicher braucht.

namespace und tolerations sind auf die Workshop-Umgebung abgestimmt.
"""

from __future__ import annotations

import pendulum
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import DAG
from kubernetes.client import models as k8s

TOLERATIONS = [
    k8s.V1Toleration(
        key="oci.oraclecloud.com/oke-is-preemptible", operator="Exists", effect="NoSchedule"
    )
]

with DAG(
    dag_id="beispiel_13_kubernetes_pod",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "kubernetes"],
):
    shell_pod = KubernetesPodOperator(
        task_id="shell_im_pod",
        name="shell-pod",
        namespace="airflow-workshop",
        image="alpine:3.18",
        cmds=["/bin/sh", "-c"],
        arguments=['echo "Hallo aus dem Pod am {{ logical_date | ds }}"'],
        get_logs=True,
        on_finish_action="delete_pod",
        tolerations=TOLERATIONS,
    )

    python_pod = KubernetesPodOperator(
        task_id="python_im_pod",
        name="python-pod",
        namespace="airflow-workshop",
        image="python:3.12-slim",
        cmds=["python", "-c"],
        arguments=["import sys; print('Python', sys.version)"],
        env_vars={"STAGE": "workshop"},
        container_resources=k8s.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "128Mi"},
            limits={"cpu": "500m", "memory": "256Mi"},
        ),
        get_logs=True,
        on_finish_action="delete_pod",
        tolerations=TOLERATIONS,
    )

    shell_pod >> python_pod
