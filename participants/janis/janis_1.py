from airflow.sdk import dag, task


@dag(
    dag_id="janis1",
    tags=["janis", "mein_dag", "ordix"]
)
def mein_dag():
    
    @task
    def doing_1():
        
        text = "Hello 1"
        print(text)
        return text

    @task
    def doing_2(txt: str):
        print("Hello 2" + txt)

    doing_2(doing_1())

mein_dag()
