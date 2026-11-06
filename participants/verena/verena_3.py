from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
import pendulum 
from airflow.sdk import get_current_context
import os






@dag(
    dag_id="verena_3",
    schedule="20 * * * *",
    start_date=pendulum.datetime(2026, 11, 5, 12, 0, tz="Europe/Berlin"),
    catchup=False,
    max_active_tasks=1,
    tags=["test", "verena"]
)
def mein_dag(): 

    @task
    def get_time():
        print("hallo")
        context = get_current_context()
        logical_date = context["logical_date"]
        ti = context["ti"]
        print(context["logical_date"])
        ti.xcom_push(key="ld", value=logical_date)
        return None

    def get_offset():
        offset = 1

    @task.sensor(poke_interval=30, timeout=600, mode="reschedule")
    def warte_auf_datei() -> bool:
        context = get_current_context()
        ti = context["ti"]
        time_var = ti.xcom_pull(task_ids="get_time", key="ld") 
        filename = f"/tmp/input_{time_var}.csv"
        print(f"waiting for file {filename}")
        return os.path.exists(filename)

    get_time() >> warte_auf_datei()

mein_dag()    