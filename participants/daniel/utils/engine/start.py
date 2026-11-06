from airflow.sdk import dag, task, get_current_context
from airflow.utils.trigger_rule import TriggerRule
import os

@task
def doing0():
    month_day = 3
    print(f"Ich starte eine tolle ETL am {month_day}")

if __name__ == "__main__":
    doing0()