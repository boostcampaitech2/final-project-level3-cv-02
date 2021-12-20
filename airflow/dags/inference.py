# inference.py

import pendulum
from datetime import time, timedelta, datetime

from airflow import DAG 
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, task
# from ...babygan import inference

kst = pendulum.timezone("Asia/Seoul")

with DAG(
    dag_id='babygan_inference',
    description='babygan inference',
    start_date=days_ago(2),
    schedule_interval='0 9 * * *',
    tags=['final_project'],
)as dag:


    t1 = BashOperator(
        task_id='inference',
        bash_command="""
        sh $AIRFLOW_HOME/dags/scripts/inference.sh
        """,
        depends_on_past=True,
        owner='ujin',
        retries=2,
        retry_delay=timedelta(minutes=5),
    )

    t1