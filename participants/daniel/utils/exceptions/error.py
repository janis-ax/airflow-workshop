from airflow.sdk import dag, task

@task(trigger_rule=TriggerRule.ONE_FAILED)
def error():
    print("Es ist ein Fehler in der Prozessierung aufgetreten")