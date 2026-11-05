from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
import pendulum


def do_something():
    print("welcome")
    return None



@dag(
    dag_id="verena_2",
    schedule="20 * * * *",
    start_date=pendulum.datetime(2026, 11, 5, 12, 0, tz="Europe/Berlin"),
    catchup=False,
    tags=["test", "verena"]
)
def mein_dag(): 
    
    first_task_task = PythonOperator(task_id="first_task", python_callable=do_something)
    second_task_task = BashOperator(task_id="bash_task", bash_command= 'echo hello')

    ### mix in decorators
    @task 
    def print_bash_output_in_python(txt: str):
        print(txt) 
        return None

    first_task_task >> print_bash_output_in_python(second_task_task.output)
    
mein_dag()    