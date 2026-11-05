"""
Beispiel 05: Jinja-Templates und Params

- Templates ({{ ... }}) werden erst zur Laufzeit gerendert
- Params sind Eingabefelder, die man beim manuellen Triggern ausfüllen kann
- In der UI: Task anklicken > "Rendered Template" zeigt das Ergebnis
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import Param, dag, task


@dag(
    dag_id="beispiel_05_templates_und_params",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule="@daily",
    catchup=False,
    params={
        "land": Param("DE", type="string", enum=["DE", "AT", "CH"], description="Ländercode"),
        "anzahl": Param(3, type="integer", minimum=1, maximum=10),
        "testlauf": Param(True, type="boolean"),
    },
    tags=["beispiel", "templates", "params"],
)
def templates_und_params():
    BashOperator(
        task_id="templates_in_bash",
        bash_command=(
            'echo "Datum:        {{ logical_date | ds }}" && '
            'echo "Intervall:    {{ data_interval_start }} bis {{ data_interval_end }}" && '
            'echo "Vortag:       {{ macros.ds_add(ds, -1) }}" && '
            'echo "Land (Param): {{ params.land }}" && '
            'echo "Run-ID:       {{ run_id }}"'
        ),
    )

    # In @task-Funktionen kommt der Kontext einfach als Parameter
    @task
    def params_in_python(params=None, ds=None):
        modus = "Testlauf" if params["testlauf"] else "echter Lauf"
        print(f"{modus} am {ds}: {params['anzahl']} Datensätze für {params['land']}")

    params_in_python()


templates_und_params()
