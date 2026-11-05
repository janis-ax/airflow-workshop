from airflow.sdk import dag, task

@dag(
    dag_id="daniel_2", 
    schedule=None,
    tags=["test", "daniel"]
)
def mein_dag(): 
    
    @task
    def doing1(): 
        print("Hello 1")


    doing1()

mein_dag()    