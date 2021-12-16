# hello_world.py

from datetime import time, timedelta

from airflow import DAG 
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, task

def print_world() -> None:
    print('world')

# with 구문으로 DAG 정의 시작
with DAG(
    dag_id="hello_world",
    description='test', 
    start_date=days_ago(1),
    schedule_interval='0 13 * * *',
    tags=['my_dags'],
) as dag:

    # 테스크 정의
    # bach command로 echo hello 실행
    t1 = BashOperator(
        task_id='print_hello',
        # bash_command='echo hello',
        bash_command='sh $AIRFLOW_HOME/dags/scipts/hello.sh',
        owner='ujin',
        retries=2,
        retry_delay=timedelta(minutes=5),
    )

    # 테스크 정의
    # python 함수인 print world 실행
    t2 = PythonOperator(
        task_id='print_world',
        python_callable=print_world,
        depends_on_past=True,
        owner='ujin',
        retries=2,
        retry_delay=timedelta(minutes=5),
    )

    # task order 
    t1 >> t2