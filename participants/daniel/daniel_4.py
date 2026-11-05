from airflow.sdk import dag, task
from airflow.utils.trigger_rule import TriggerRule

@dag(
    dag_id="daniel_4",
    schedule= "20 15 * * *",
    tags=["test", "daniel"]
)
def test_etl():

    @task.bash
    def bash_test():
        return "echo 'Damit wir mal Bash getestet haben'"

    @task
    def error(trigger_rule=TriggerRule.ONE_FAILED):
        print("Es ist ein Fehler in der Prozessierung aufgetreten")

    @task
    def doing0():
        month_day = 3
        print(f"Ich starte eine tolle ETL am {month_day}")

    @task
    def doing1():
        message = 200

        if message == 200:
            return 1
        else:
            return 2

    @task
    def doing2(result):
        if result == 1:
            print("Perfect")
        else:
            print("Error")
    
    @task
    def start_alt():
        print("alternativer start")
        raise Exception("This task always fails")

    bash_task = bash_test()
    start = doing0()
    start_alt = start_alt()
    verify_message = doing1()
    interprete_message = doing2(verify_message)
    error = error()

    bash_task >> start_alt 
    bash_task >> start >> verify_message >> interprete_message 
test_etl()