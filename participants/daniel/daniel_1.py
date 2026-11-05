# import pendulum
from airflow.sdk import dag, task

@dag(
    dag_id="daniel_1",
    schedule=None,
    catchup=False,
    tags=["daniel", "test"],
)


class KlassenTest: 
    def __init__():
        pass
    @task
    def doing_1() -> None:
        print("Hello 1")

KlassenTest.doing_1()
