from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="dummy_duck",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["workshop"],
) as dag:
    BashOperator(task_id="quack", bash_command="echo 'Quack! 🦆'")
