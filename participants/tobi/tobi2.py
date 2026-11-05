from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

def hello():
    return "Hello"

def testprint():
    output = hello()
    print(output)
    BashOperator(task_id="file-write", bash_command=f"echo '{output}' >> /tmp/test.txt")

with DAG(dag_id="tobi2", tags=["tobi"]):
    schritt_1 = BashOperator(task_id="tobi_schritt_1", bash_command='touch /tmp/test.txt')
    schritt_2 = PythonOperator(task_id="schritt_2", python_callable=testprint)
    schritt_3 = BashOperator(task_id="tobi_schritt_3", bash_command='cat /tmp/test.txt')

    schritt_1 >> schritt_2 >> schritt_3
