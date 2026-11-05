"""
Musterlösung Aufgabe 10: Pod mit Env Vars und Ressourcen

- Umgebungsvariablen (env_vars sind templated, RUN_DATE wird also gerendert)
- Ressourcen-Requests und -Limits über container_resources
"""

from __future__ import annotations

import pendulum
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.sdk import DAG
from kubernetes.client import models as k8s

with DAG(
    dag_id="loesung_10_k8s_configured_pod",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["musterloesung", "aufgabe_10", "kubernetes"],
):
    KubernetesPodOperator(
        task_id="configured_pod",
        name="configured-pod",
        namespace="airflow-workshop",
        image="python:3.11-slim",
        cmds=["python", "-c"],
        arguments=[
            "import os; print('ENV:', os.getenv('ENV')); print('RUN_DATE:', os.getenv('RUN_DATE'))"
        ],
        env_vars={
            "ENV": "prod",
            "RUN_DATE": "{{ logical_date | ds }}",
        },
        container_resources=k8s.V1ResourceRequirements(
            requests={"cpu": "250m", "memory": "256Mi"},
            limits={"cpu": "500m", "memory": "512Mi"},
        ),
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
