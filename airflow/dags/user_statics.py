# inference.py

import pendulum
from datetime import time, timedelta, datetime

from airflow import DAG 
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from collections import defaultdict
from connect_db import DBController

from dotenv import load_dotenv

kst = pendulum.timezone("Asia/Seoul")
AIRFLOW_HOME = '/opt/ml/final-project-level3-cv-02/airflow'
INFER_RESULT_PATH = os.path.join(AIRFLOW_HOME, 'csv')

def load_data_from_mysql():
    controller = DBController()
    controller.load_data()
    controller.out_csv()
    return

def data_to_db(df_result, table_name):
    load_dotenv(
			dotenv_path="/opt/ml/final-project-level3-cv-02/.env",
			override=True,
			verbose=False
			)
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_PORT = os.getenv('MYSQL_PORT')
    MYSQL_DBNAME = os.getenv('MYSQL_DB')
    MYSQL_SERVER = os.getenv('MYSQL_SERVER')

    DB = pymysql.connect(host=MYSQL_SERVER, user=MYSQL_USER, passwd=MYSQL_PASSWORD, port=int(MYSQL_PORT), charset='utf8')

    engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DBNAME}?charset=utf8mb4')
    engine_conn = engine.connect()
    df_result.to_sql(table_name , engine_conn, if_exists='replace', index=None)
    engine_conn.close()
    engine.dispose()
    return 

def calculate_bounce_rate():
    print(f'calculate bounce rate after click inference button')
    df_log = pd.read_csv(os.path.join(f'{INFER_RESULT_PATH}', 'data.csv'), parse_dates = ['created_time'])

    #### ----------------------------del ------------------------------------
    df_log['age'] = df_log['age'].fillna(0)
    df_log['gender'] = df_log['gender'].fillna('male')
    #### ----------------------------del ------------------------------------

    df_log['age'] = df_log['age'].astype(int)
    total_id = len(df_log)
    df_statics = pd.DataFrame(columns = ['id', 'gender', 'age', 'rate'])

    # calculate inference_bounce_rate
    # total_b_rate = len(df_log['complete' == False]) / len(df_log) # inference_bounce_rate -> #bounce / #click_inference_button = #complete==False / #ID
    df_statics['ID'] = [i for i in range(1,11)]

    # gender - age 
    gen_age = defaultdict(str)
    gender = ['male', 'female']
    age = [10, 20,30,40,50, 100]
    gen_age['female'] = []
    gen_age['male'] = []

    total_data = []
    id = 1
    for g in gender:
        for a_i in range(len(age)-1):
            condition = (df_log.gender == g) & ((int(age[a_i]) <= df_log["age"]) & ( df_log["age"] < int(age[a_i+1])))
            rate = len(df_log[condition]) / total_id * 100
            total_data.append([id, g, age[a_i], rate])
            # gen_age[g].append(len(df_log[condition]))
            id+=1

    df_result = pd.DataFrame(total_data, columns=['id', 'gender', 'age', 'rate'])
    data_to_db(df_result, 'user_statistic')
    
    return

def analysis():
    df = pd.read_csv(os.path.join(f'{INFER_RESULT_PATH}', 'data.csv'), parse_dates=["created_time", "closed_at"])
    df["duration"] = df["closed_at"]-df["created_time"]
    grouped =  df.groupby(df["complete"])["duration"]
    avg_bounce, avg_inference = grouped.sum()/grouped.size()
    total = len(df)
    df_result = pd.DataFrame([avg_bounce,total, avg_inference], columns=["avg_bounce_time", "total_user", "avg_inference_time"])
    data_to_db(df_result, 'statistic')
    
    return


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
    load_data_from_db_task = PythonOperator(
        task_id = 'load_data_from_db',
        python_callable=load_data_from_mysql,
        dag=mysql_dag,
    )

    calculate_bounce_rate_task = PythonOperator(
        task_id = 'calculate_bounce_rate',
        python_callable=calculate_bounce_rate,
        dag=mysql_dag,
    )

    analysis_task = PythonOperator(
        task_id = 'calculate_total_bounce_and_infer_rate',
        python_callable=analysis,
        dag=mysql_dag,
    )


    load_data_from_db_task >> calculate_bounce_rate_task
    load_data_from_db_task >> analysis_task



'''
sql
1. /scripts/get_inference_result.sql -> jinja2.exceptions.TemplateNotFound: /scripts/get_inference_result.sql

2. '$AIRFLOW_HOME/dags/scripts/get_inference_result.sql' -> jinja2.exceptions.TemplateNotFound: $AIRFLOW_HOME/dags/scripts/get_inference_result.sql

3. sql=r"""select * from inference_result;""" -> airflow.exceptions.AirflowNotFoundException: The conn_id `mysql_conn_id` isn't defined

-> export AIRFLOW_CONN_MYSQL_DEFAULT='mysql+mysqldb://cv02:boostcampcv02@cv02.cufn2thqplnf.ap-northeast-2.rds.amazonaws.com:3306/cv02'

'''
