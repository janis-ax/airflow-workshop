from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator


def do_something():
    print("welcome")
    return None


def do_something_in_bash():
    return 'echo "hello"'



@dag(
    dag_id="verena_2", 
    schedule=None,
    tags=["test", "verena"]
)
def mein_dag(): 
    
    first_task_task = PythonOperator(task_id="first_task", python_callable=do_something)
    second_task_task = BashOperator(task_id="bash_task", bash_command=do_something_in_bash)

    ### mix in decorators
    @task 
    def print_bash_output_in_python(txt: str):
        print(txt) 
        return None


    first_task_task >> second_task_task 
# print_bash_output_in_python(second_task_task.output)
    
mein_dag()    