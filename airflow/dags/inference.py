# inference.py

import pendulum
from datetime import time, timedelta, datetime

from airflow import DAG 
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, task
# from ...babygan import inference

# 한국 시간 timezone 설정
kst = pendulum.timezone("Asia/Seoul")

with DAG(
    dag_id='babygan_inference',
    description='babygan inference',
    # start_date=days_ago(2),
    start_date=datetime(2021, 12, 14, tzinfo=kst), # 2021.12.15일부터 시작
    schedule_interval='0 9 * * *', # 매일 오전 9시 마다
    tags=['final_project'],
)as dag:


    t1 = BashOperator(
        task_id='inference',
        bash_command="""
            sh $AIRFLOW_HOME/dags/scipts/inference.sh
        """,
        depends_on_past=True,
        owner='ujin',
        retries=2,
        retry_delay=timedelta(minutes=5),
    )

    t1