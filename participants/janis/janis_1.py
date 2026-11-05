from airflow.sdk import dag, task


@dag(
    dag_id="janis1",
    tags=["janis", "mein_dag", "ordix"]
)
def mein_dag():
    
    @task
    def doing_1():
        print("Hello 1")

    doing_1()

mein_dag()
