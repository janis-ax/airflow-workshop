from airflow.sdk import dag, task

@dag(
    dag_id="daniel_2", 
    schedule=None,
    tags=["test", "daniel"]
)
def mein_dag(): 
    
    @task
    def doing1(): 
        message = 200
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

    result = doing1()
    doing2()

mein_dag()    