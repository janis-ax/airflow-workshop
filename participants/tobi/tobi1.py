from airflow.sdk import dag, task

@dag(
    dag_id="tobi1",
    tags=["test", "test2", "test3"]
)
def mydag():
    @task
    def doing_1():
        print("Hello")

    doing_1()

mydag()