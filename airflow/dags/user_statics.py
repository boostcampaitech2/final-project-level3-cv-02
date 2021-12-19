# inference.py

import pendulum
from datetime import time, timedelta, datetime

from airflow import DAG 
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.python import PythonOperator
from airflow.models.variable import Variable

import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from collections import defaultdict

# .env
from dotenv import load_dotenv
load_dotenv(dotenv_path = ".env")
access_key_id = os.getenv('access_key_ID')
access_key_pass = os.getenv('access_key_PASS')

kst = pendulum.timezone("Asia/Seoul")
AIRFLOW_HOME = ' /opt/ml/final-project-level3-cv-02/airflow'
INFER_RESULT_PATH = os.path.join(AIRFLOW_HOME, 'infer_result')

def connect_db_get_data():
    # user_nm = 'admin'
    # passwd = 'celebdbteam2@#'
    # host_url = 'db.ds.mycelebs.com'
    # port_num = 3306
    # db_name = 'book_kyobo'

    # Variable
    MYSQL_USER_ID = Variable.get("MYSQL_USER_ID")
    MYSQL_PASSWORD = Variable.get("MYSQL_PASSWORD")
    MYSQL_PORT = Variable.get("MYSQL_PORT")
    MYSQL_DBNAME = Variable.get("MYSQL_DBNAME")
    MYSQL_SERVER = Variable.get("MYSQL_SERVER")

    DB = pymysql.connect(host=MYSQL_SERVER, user=MYSQL_USER_ID, passwd=MYSQL_PASSWORD, port=int(MYSQL_PORT), charset='utf8')

    data = pd.read_sql('''
    select * from cv02.inference_result''', con = DB)
    print(data.shape[0])

    os.mkdir(INFER_RESULT_PATH, exist_ok=True)
    data.to_csv(f'{AIRFLOW_HOME}/infer_result/infer_result_latest.csv', index=False)
    print(f'save inference_result_latest in {INFER_RESULT_PATH}')
    return 
   

def calculate_bounce_rate(result):
    print(f'calculate bounce rate after click inference button')
    df_log = pd.read_csv(f'{AIRFLOW_HOME}/infer_result/infer_result_latest.csv')
    df_statics = pd.DataFrame(columns = ['ID', 'age', 'gender', 'inference_bounce_rate'])

    # calculate inference_bounce_rate
    total_b_rate = len(df_log['compelete' == False]) / len(df_log) # inference_bounce_rate -> #bounce / #click_inference_button = #complete==False / #ID
    df_statics['ID'] = [i for i in range(1,11)]

    # gender - age 
    gen_age = defaultdict(str)
    age = [20,30,40,50]
    gen_age['female'] = []
    for a in age:
        gen_age['female'].append(df_log['gender' == 'female' and 'age' < 20]) 


    return


def data_to_db(INFER_RESULT_PATH):
    MYSQL_USER_ID = Variable.get("MYSQL_USER_ID")
    MYSQL_PASSWORD = Variable.get("MYSQL_PASSWORD")
    MYSQL_PORT = Variable.get("MYSQL_PORT")
    MYSQL_DBNAME = Variable.get("MYSQL_DBNAME")
    MYSQL_SERVER = Variable.get("MYSQL_SERVER")

    DB = pymysql.connect(host=MYSQL_SERVER, user=MYSQL_USER_ID, passwd=MYSQL_PASSWORD, port=int(MYSQL_PORT), charset='utf8')

    infer_df = pd.read_csv(INFER_RESULT_PATH)

    engine = create_engine()
    engine_conn = engine.connect(f'mysql+pymysql://{MYSQL_USER_ID}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DBNAME}?charset=utf8mb4')
    infer_df.to_sql('inference_bounce_rate', engine_conn, if_exists='replace', index=None)
    engine_conn.close()
    engine.dispose()


default_args = {
    'owner': 'ujin',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

default_args_sql = {
    'owner': 'ujin',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
    dag_id='user_statics',
    description='get user statics',
    start_date=days_ago(1),
    schedule_interval='0 22 * * *',
    default_args=default_args_sql,
    tags=['final_project'],
    catchup=False,
) as mysql_dag:


# # TODO 
# get_infer_result_task = MySqlOperator(
#     task_id = 'get_infer_result',
#     sql=r"""select * from inference_result;""",
#     dag=mysql_dag,
# )

    # this
    get_infer_result_pymysql_task = PythonOperator(
        task_id = 'get_infer_result',
        python_callable=connect_db_get_data,
        dag=mysql_dag,
    )

    calculate_bounce_rate_task = PythonOperator(
        task_id = 'calculate_bouce_rate',
        python_callable=calculate_bounce_rate,
        dag=mysql_dag,
    )

    data_to_db_task = PythonOperator(
        task_id = 'calculate_bouce_rate',
        python_callable=data_to_db,
        dag=mysql_dag,
    )

    get_infer_result_pymysql_task >> calculate_bounce_rate_task >> data_to_db_task

'''
sql
1. /scripts/get_inference_result.sql -> jinja2.exceptions.TemplateNotFound: /scripts/get_inference_result.sql

2. '$AIRFLOW_HOME/dags/scripts/get_inference_result.sql' -> jinja2.exceptions.TemplateNotFound: $AIRFLOW_HOME/dags/scripts/get_inference_result.sql

3. sql=r"""select * from inference_result;""" -> airflow.exceptions.AirflowNotFoundException: The conn_id `mysql_conn_id` isn't defined

-> export AIRFLOW_CONN_MYSQL_DEFAULT='mysql+mysqldb://cv02:boostcampcv02@cv02.cufn2thqplnf.ap-northeast-2.rds.amazonaws.com:3306/cv02'

'''
