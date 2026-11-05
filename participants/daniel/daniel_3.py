from airflow.sdk import dag, task

@dag(
    dag_id="daniel_3",
    schedule=None,
    tags=["test", "daniel"]
)
def test_etl():

    @task.bash
    def bash_test():
        return "echo 'Damit wir mal Bash getestet haben'"

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

    bash_task = bash_test()
    start = doing0()
    verify_message = doing1()
    interprete_message = doing2(verify_message)

    bash_task >> start
    bash_task >> start >> verify_message >> interprete_message

test_etl()