from airflow.sdk import dag, task, get_current_context
from airflow.utils.trigger_rule import TriggerRule, get_current_context
import os

@dag(
    dag_id="daniel_6",
    schedule= "20 15 * * *",
    tags=["test", "daniel"]
)
def test_etl():



    # Sensor für Deffered Action prüfen
    @task.sensor(poke_interval=30, timeout=600, mode="reschedule")
    def warte_auf_datei() -> bool:
        return os.path.exists("/tmp/input.csv")

    @task.bash
    def bash_test():
        return "echo 'Damit wir mal Bash getestet haben'"

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def error():
        print("Es ist ein Fehler in der Prozessierung aufgetreten")

    @task
    def doing0():
        month_day = 3
        print(f"Ich starte eine tolle ETL am {month_day}")

    # XCOM Datenübergabe testen
    @task
    def doing1():
        context = get_current_context()
        ti = context["ti"]

        message = 200

        ti.xcom_push(key="status_code", value=message)

        if message == 200:
            return 1
        else:
            return 2
        

    # XCOM Empfang testen
    @task
    def doing2(result):
        context = get_current_context()
        ti = context["ti"]
        if result == 1:
            print("Perfect")
        else:
            print("Error")

        status_code = ti.xcom_pull(
            task_ids="doing1",
            key="status_code"
        )

        print(f"Statuscode aus XCOM ist: {status_code}")
    
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
    wait = warte_auf_datei()

    bash_task >> start_alt >> error
    bash_task >> start >> wait >> verify_message >> interprete_message
test_etl()