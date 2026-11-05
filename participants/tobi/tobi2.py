from airflow.providers.standard.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

def hello():
    print("Hello")
    return "Hello"

def testprint():
    hello()

with DAG(dag_id="tobi2", tags=["tobi"]):
    schritt_1 = BashOperator(task_id=tobi_schritt_1, bash_command='touch "/tmp/test.txt')
    schritt_2 = PythonOperator(task_id="schritt_2", python_callable=testprint)
