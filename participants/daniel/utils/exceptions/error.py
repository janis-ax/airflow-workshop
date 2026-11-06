from airflow.sdk import dag, task
from airflow.utils.trigger_rule import TriggerRule


@task(trigger_rule=TriggerRule.ONE_FAILED)
def error():
    print("Es ist ein Fehler in der Prozessierung aufgetreten")