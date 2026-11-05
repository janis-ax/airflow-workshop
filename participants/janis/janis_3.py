
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG



def tu_was1():
    print("Hello Hello")


with DAG(dag_id="janis_3", tags=["janis", "mein_dag", "ordix"], description="bla"):

    doing_1 = PythonOperator(task_id="task1", python_callable=tu_was1)
    doing_2 = PythonOperator(task_id="task2", python_callable=tu_was1)

    doing_2 >> doing_1
