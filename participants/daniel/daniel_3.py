from airflow.sdk import dag, task

@dag(
    dag_id="daniel_2", 
    schedule=None,
    tags=["test", "daniel"]
)
def test_etl(): 

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

    start = doing0()
    verify_message = doing1()
    interprete_message = doing2(result)

    start >> verify_message >> interprete_message


test_etl()    