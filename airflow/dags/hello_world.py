# hello_world.py

import pendulum
from datetime import time, timedelta, datetime

from airflow import DAG 
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, task

kst = pendulum.timezone("Asia/Seoul")

def print_world() -> None:
    print('world')

with DAG(
    dag_id="hello_world",
    description='test', 
    start_date=days_ago(1),
    # start_date=(2021, 12, 14, tzinfo=kst),
    schedule_interval='0 13 * * *',
    tags=['my_dags'],
) as dag:

    t1 = BashOperator(
        task_id='print_hello',
        # 2. https://www.bucketplace.co.kr/post/2021-04-13-%EB%B2%84%ED%82%B7%ED%94%8C%EB%A0%88%EC%9D%B4%EC%8A%A4-airflow-%EB%8F%84%EC%9E%85%EA%B8%B0/
        bash_command="""
        sh $AIRFLOW_HOME/dags/scripts/test.sh
        """,
        owner='ujin',
        retries=2,
        retry_delay=timedelta(minutes=1),
    )

    # t1 = BashOperator(
    #     task_id='print_hello',
    #     bash_command='pwd',
    #     owner='ujin',
    #     retries=2,
    #     retry_delay=timedelta(minutes=5),
    # )

    t2 = PythonOperator(
        task_id='print_world',
        python_callable=print_world,
        depends_on_past=True,
        owner='ujin',
        retries=2,
        retry_delay=timedelta(minutes=1),
    )

    # task order 
    t1 >> t2