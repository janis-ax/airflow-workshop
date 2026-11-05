from airflow.sdk import dag, task


@dag(
    dag_id="janis2",
    tags=["janis", "mein_dag", "ordix"],
)
def mein_dag():

    @task
    def doing_1():
        text = "Hello 1"
        print(text)
        return text

    @task
    def doing_2(txt: str):
        print(type(d1))
        print("Hello 2 " + txt)

    @task
    def doing_3():
        print("hello 3")

    @task
    def doing_4():
        print("Hello 4")

    d1 = doing_1()  

    print(type(d1))               

    doing_2(d1)                    
    d1 >> doing_3() >> doing_4()  


mein_dag()