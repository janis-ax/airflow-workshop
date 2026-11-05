from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator

@dag(
    dag_id="daniel_3", 
    schedule=None,
    tags=["test", "daniel"]
)
def test_etl(): 

    @task.bash
    def bash_test():
        return "echo 'Damit mir mal Bash getestet haben'"

    @task
    def doing0():
        month_day = 3
        print(f"Ich starte eine tolle ETL am {month_day}")
    
    @task
    def doing1(): 
        message = 200
        result = None
        if message == 200:
            result = 1
        else:
            result = 2
        return result
    
    @task
    def doing2(result):
        if result == 1:
            print("Perfect")
        else:
            print("Error")

    bash_test = bash_test()
    start = doing0()
    verify_message = doing1()
    interprete_message = doing2(result)

    bash_test >> start >> verify_message >> interprete_message


test_etl()    