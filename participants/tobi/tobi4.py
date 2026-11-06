from airflow.sdk import dag, task

@dag(
    dag_id="tobi4",
    tags=["test", "test2", "test3"]
)
def mydag():

    @task
    def doing_1(counter):
        counter += 1
        print("Hello")
        return doing_2(counter)

    @task
    def doing_2(counter):
        counter += 1
        print("World")
        if counter > 100:
            raise SystemError("100 reached")
        else:
            return doing_1(counter)

    doing_2(1)

mydag()