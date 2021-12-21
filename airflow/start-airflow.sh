#!/bin/sh
# nohup airflow standalone 1>/dev/null 2>&1 &

nohup airflow webserver --port 6006 1>/dev/null 2>&1 &
nohup airflow scheduler 1>/dev/null 2>&1 &