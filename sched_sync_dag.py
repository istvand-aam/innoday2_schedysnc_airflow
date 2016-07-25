from airflow import DAG
from airflow.operators import PythonOperator, PostgresOperator

SchedSyncDAG = DAG('Fake Schedule Sync')  # TODO default args

# let's try with Python/Postgres operators first

task_0_pull_pos_feed = PythonOperator(...)

task_1_create_templates_for_schedules = PythonOperator(...)



