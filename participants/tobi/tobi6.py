from airflow.sdk import dag, task

@dag(
    dag_id="tobi6",
    tags=["test", "test2", "test3"]
)
def mydag():
    @task
    def doing_1():
        # Pushen
        ti.xcom_push(key="alter", value=65)
        ti.xcom_push(key="name", value="franz")
        ti.xcom_push(key="lieblingszahl", value=3.14)
.
    @task
    def doing_2():
        # Pull
        alter = ti.xcom_pull(task_ids="doing_1", key="alter")
        name = ti.xcom_pull(task_ids="doing_1", key="name")
        lieblingszahl = ti.xcom_pull(task_ids="doing_1", key="lieblingszahl")

        return_string = f"Hello my name is {name}. {alter} years old. My favourite number is {lieblingszahl}."
        return return_string

    doing_1() >> doing_2()

mydag()