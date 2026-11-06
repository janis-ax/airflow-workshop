from airflow.sdk import dag, task

@dag(
    dag_id="tobi5",
    tags=["test", "test2", "test3"]
)
def mydag():
    @task
    def doing_1():
        print("Hello")

    @task.sensor(poke_interval=30, timeout=600, mode="reschedule")
    def warte_auf_datei() -> bool:
        return os.path.exists("/tmp/input.csv")

    doing_1() >> warte_auf_datei()

mydag()