from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators import PythonOperator, SimpleHttpOperator
# you need to add stuff to pythonpath :(
from sched_sync_functions import pull_pos_feed, create_playlists, create_schedules, cleanup_schedules

SchedSyncDAG = DAG('Fake_Schedule_Sync')  # TODO default args?

MANANA = (datetime.now() + timedelta(days=1))

# let's try with Python and HTTP operators

# result: pos sessions
task_pull_pos_feed = PythonOperator(
    task_id='pull_pos_feed',
    python_callable=pull_pos_feed,
    start_date=MANANA,
    op_kwargs={},
    dag=SchedSyncDAG
)

# result: SPLs with content
task_create_playlists = PythonOperator(
    task_id='create_playlist',
    python_callable=create_playlists,
    start_date=MANANA,
    op_kwargs={},
    dag=SchedSyncDAG
)

# result: schedules (shows) with assigned SPLs
task_create_schedules = PythonOperator(
    task_id='create_schedules',
    python_callable=create_schedules,
    start_date=MANANA,
    op_kwargs={},
    dag=SchedSyncDAG
)

# result: schedules (SPL-startdatetime-screenid) on the device
task_send_schedules_to_screen = SimpleHttpOperator(
    task_id='send_schedules_to_screen',
    endpoint='127.0.0.1',
    start_date=MANANA,
    dag=SchedSyncDAG
)

# result: clean slate on the (sms of the) screen - no schedules
task_cleanup_previous_schedules = SimpleHttpOperator(
    task_id='cleanup_schedules',
    endpoint='127.0.0.1',
    start_date=MANANA,
    dag=SchedSyncDAG
)

# Dependencies among tasks
task_create_schedules.set_upstream(task_create_playlists)
task_create_schedules.set_upstream(task_cleanup_previous_schedules)
task_create_schedules.set_upstream(task_pull_pos_feed)
task_send_schedules_to_screen.set_upstream(task_create_schedules)
