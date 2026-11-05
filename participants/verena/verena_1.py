from airflow.sdk import dag, task

@dag(
    dag_id="verena_1", 
    schedule=None,
    tags=["test", "verena"]
)
def mein_dag(): 
    
    @task
    def doing1(): 
        print("Hello 1")

    @task
    def doing2():
        print("Hello x2")

    doing2(doing1())

mein_dag()    