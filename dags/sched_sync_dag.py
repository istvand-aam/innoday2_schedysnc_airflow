from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators import PythonOperator, SimpleHttpOperator
# you need to add stuff to pythonpath :(
from sched_sync_functions import pull_pos_feed, create_playlists, create_schedules, send_schedules_to_screen

MANANA = (datetime.now() + timedelta(days=1))

SchedSyncDAG = DAG('Fake_Schedule_Sync',
    schedule_interval=timedelta(10),
    start_date=datetime.now() + timedelta(seconds=20),
    default_args={
    'start_date': datetime.now() + timedelta(seconds=20),
    'owner': 'TMS'
    }
)

# let's try with Python and HTTP operators

# result: pos sessions
task_pull_pos_feed = PythonOperator(
    task_id='pull_pos_feed',
    python_callable=pull_pos_feed,
    op_kwargs={},
    dag=SchedSyncDAG
)

# result: SPLs with content
task_create_playlists = PythonOperator(
    task_id='create_playlists',
    python_callable=create_playlists,
    op_kwargs={},
    dag=SchedSyncDAG
)

# result: schedules (shows) with assigned SPLs
task_create_schedules = PythonOperator(
    task_id='create_schedules',
    provide_context=True,
    python_callable=create_schedules,
    op_kwargs={},
    dag=SchedSyncDAG
)

# result: schedules (SPL-startdatetime-screenid) on the device
# needed to add this as PythonOp instead of HTTP because data needs to be passed through via XCom
# and HTTPOperator cannot receive stuff easily (as we know Airflow now:)
task_send_schedules_to_screen = PythonOperator(
    task_id='send_schedules_to_screen',
    python_callable=send_schedules_to_screen,
    provide_context=True,
    op_kwargs=dict(
        http_conn_id='screen_server',
        endpoint='api/schedules',
        headers={"Content-Type": "application/json"},
        method='POST'
    ),
    dag=SchedSyncDAG
)

# result: clean slate on the (sms of the) screen - no schedules
task_cleanup_previous_schedules = SimpleHttpOperator(
    task_id='cleanup_schedules',
    http_conn_id='screen_server',
    endpoint='api/schedules/clear',
    method='GET',
    dag=SchedSyncDAG
)

# Dependencies among tasks
task_create_schedules.set_upstream(task_create_playlists)
task_create_schedules.set_upstream(task_cleanup_previous_schedules)
task_create_schedules.set_upstream(task_pull_pos_feed)
task_send_schedules_to_screen.set_upstream(task_create_schedules)
