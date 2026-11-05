"""
Beispiel 04: Daten zwischen Tasks weitergeben (XCom)

Drei Varianten:
1. TaskFlow: return + Parameter (empfohlen)
2. Mehrere Rückgabewerte mit multiple_outputs
3. Klassisch: Ergebnis eines Operators per .output oder im Template per xcom_pull

Merke: XComs liegen in der Metadaten-Datenbank. Nur kleine Werte
übergeben (IDs, Pfade, Zähler), keine großen Datenmengen.
"""

from __future__ import annotations

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag, task


@dag(
    dag_id="beispiel_04_xcom_daten_weitergeben",
    start_date=pendulum.datetime(2024, 1, 1, tz="Europe/Berlin"),
    schedule=None,
    catchup=False,
    tags=["beispiel", "xcom"],
)
def xcom_beispiel():
    # 1) Einfach: return und Parameter
    @task
    def extract() -> list[int]:
        return [3, 7, 12]

    @task
    def transform(zahlen: list[int]) -> int:
        return sum(zahlen)

    # 2) multiple_outputs: jeder Schlüssel wird ein eigener XCom
    @task(multiple_outputs=True)
    def statistik(zahlen: list[int]) -> dict:
        return {"minimum": min(zahlen), "maximum": max(zahlen)}

    @task
    def load(summe: int, minimum: int, maximum: int):
        print(f"Summe {summe}, Minimum {minimum}, Maximum {maximum}")

    zahlen = extract()
    stats = statistik(zahlen)
    summe = transform(zahlen)
    load(summe, stats["minimum"], stats["maximum"])

    # 3) Klassischer Operator: letzte Ausgabezeile von Bash landet als XCom
    zaehle = BashOperator(task_id="zaehle_dateien", bash_command="ls /tmp | wc -l")

    @task
    def zeige_anzahl(anzahl: str):
        print(f"In /tmp liegen {anzahl.strip()} Einträge")

    zeige_anzahl(zaehle.output)

    # ... und im Template per xcom_pull
    BashOperator(
        task_id="template_xcom",
        bash_command="echo \"Summe laut XCom: {{ ti.xcom_pull(task_ids='transform') }}\"",
    ).set_upstream(summe)


xcom_beispiel()
