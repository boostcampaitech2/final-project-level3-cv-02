# user_statics.py

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

def load_data_from_mysql(table_name):
    controller = DBController()
    controller.load_data(table_name)
    controller.out_csv()
    return

def data_to_db(df_result, table_name):
    controller = DBController()
    controller.save_data_to_db(df_result, table_name)

    return 

def calculate_bounce_rate():
    print(f'calculate bounce rate after click inference button')
    df_log = pd.read_csv(os.path.join(f'{INFER_RESULT_PATH}', 'data.csv'), parse_dates = ['created_time'])

    df_log['age'] = df_log['age'].astype(int)
    total_id = len(df_log)

    # gender - age 
    gender = ['male', 'female']
    age = [10, 20,30,40,50, 100]
    total_data = []
    id = 1
    for g in gender:
        for a_i in range(len(age)-1):
            condition = (df_log.gender == g) & ((int(age[a_i]) <= df_log["age"]) & ( df_log["age"] < int(age[a_i+1])))
            rate = len(df_log[condition]) / total_id * 100
            total_data.append([id, g, age[a_i], rate])
            id+=1

    df_result = pd.DataFrame(total_data, columns=['id', 'gender', 'age', 'rate'])
    data_to_db(df_result, 'user_statistic')
    
    return

def analysis():
    df = pd.read_csv(os.path.join(f'{INFER_RESULT_PATH}', 'data.csv'), parse_dates=["created_time", "closed_at"])
    df["duration"] = df["closed_at"]-df["created_time"]
    grouped =  df.groupby(df["complete"])["duration"]
    avg = grouped.sum()/grouped.size()
    try:
        avg_bounce = avg[0]
    except KeyError:
        avg_bounce = 0
    try:
        avg_inference = avg[1]
    except KeyError:
        avg_inference = 0
    
    total = len(df)
    df_result = pd.DataFrame([[avg_bounce,total, avg_inference]], columns=["avg_bounce_time", "total_user", "avg_inference_time"])
    data_to_db(df_result, 'statistic')
    
    return

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

    load_data_from_db_task = PythonOperator(
        task_id = 'load_data_from_db',
        python_callable=load_data_from_mysql,
        op_kwargs={'table_name': 'inference_result'},
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

