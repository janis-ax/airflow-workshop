from airflow.sdk import dag, task
from utils import tobi_lib

tl = tobi_lib

@dag(
    dag_id="tobi7"
)
def mydag():
    @task
    def doing_1():
        tl.hello_world()

    @task
    def doing_2():
        tl.doing_2(1)

    doing_1()
    doing_2()


mydag()