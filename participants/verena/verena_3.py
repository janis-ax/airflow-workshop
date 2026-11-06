from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
import pendulum 
from airflow.sdk import get_current_context



def do_something():
    print("hallo")
    context = get_current_context()
    print(context["logical_date"])
    return None



@dag(
    dag_id="verena_3",
    schedule="20 * * * *",
    start_date=pendulum.datetime(2026, 11, 5, 12, 0, tz="Europe/Berlin"),
    catchup=True,
    max_active_tasks=1,
    tags=["test", "verena"]
)
def mein_dag(): 
    
    first_task_task = PythonOperator(task_id="first_task", python_callable=do_something)

    @task.sensor(poke_interval=30, timeout=600, mode="reschedule")
    #def warte_auf_datei() -> bool:
    #    return os.path.exists("/tmp/input.csv")

    first_task_task >> warte_auf_datei

mein_dag()    