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

# .env
from dotenv import load_dotenv
load_dotenv(dotenv_path = ".env")
access_key_id = os.getenv('access_key_ID')
access_key_pass = os.getenv('access_key_PASS')



kst = pendulum.timezone("Asia/Seoul")

def connect_db():
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

    return data

def image_download_from_s3():   
    pass


def data_preprocessing(result):
    df = pd.DataFrame()
    return df

def data_to_db():
    pass

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

mysql_dag = DAG(
    dag_id='user_statics',
    description='get user statics',
    start_date=days_ago(1),
    schedule_interval='0 22 * * *',
    default_args=default_args_sql,
    tags=['final_project'],
    catchup=False,
)

# # TODO 
# get_infer_result_task = MySqlOperator(
#     task_id = 'get_infer_result',
#     sql=r"""select * from inference_result;""",
#     dag=mysql_dag,
# )

# this
get_infer_result_pymysql_task = PythonOperator(
    task_id = 'get_infer_result',
    python_callable=connect_db,
    dag=mysql_dag,
)


get_infer_result_pymysql_task

'''
sql
1. /scripts/get_inference_result.sql -> jinja2.exceptions.TemplateNotFound: /scripts/get_inference_result.sql

2. '$AIRFLOW_HOME/dags/scripts/get_inference_result.sql' -> jinja2.exceptions.TemplateNotFound: $AIRFLOW_HOME/dags/scripts/get_inference_result.sql

3. sql=r"""select * from inference_result;""" -> airflow.exceptions.AirflowNotFoundException: The conn_id `mysql_conn_id` isn't defined

-> export AIRFLOW_CONN_MYSQL_DEFAULT='mysql+mysqldb://cv02:boostcampcv02@cv02.cufn2thqplnf.ap-northeast-2.rds.amazonaws.com:3306/cv02'

'''
