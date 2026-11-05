import pendulum
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG, get_current_context


def tu_was1():
    print(f"Jetzt ist es {pendulum.now()}")


def was_steht_im_context():
    print(get_current_context())


def logical_date_ist():
    print(get_current_context()["logical_date"])


def gestern_berechnen():
    c = get_current_context()
    log_date = c["logical_date"]

    d = pendulum.instance(log_date)
    d = d.in_timezone("Europe/Berlin")
    gestern = d.subtract(days=1).to_date_string()

    print(gestern)


with DAG(
    dag_id="janis_4",
    start_date=pendulum.datetime(2026, 11, 1, tz="Europe/Berlin"),
    schedule="@daily",
    catchup=True,
    tags=["janis", "mein_dag", "ordix"],
    description="Toller DAG mit Context",
):
    doing_1 = PythonOperator(task_id="task1", python_callable=tu_was1)
    doing_2 = PythonOperator(task_id="task2", python_callable=was_steht_im_context)
    doing_3 = PythonOperator(task_id="task3", python_callable=logical_date_ist)
    doing_4 = PythonOperator(task_id="task4", python_callable=gestern_berechnen)

    doing_1 >> [doing_2, doing_3, doing_4]