# Python functions used by Sched Sync DAG are here

from datetime import datetime, timedelta
import json
from uuid import uuid4

import requests
from faker_cinema import FakerCinema

TODAY = datetime.today()

EIGHT_O_CLOCK = datetime(TODAY.year, TODAY.month, TODAY.day, 20, 0, 0)

CREDENTIALS = {
    'user': 'admin',
    'password': 'admin'
}

FAKER = FakerCinema()


CONTENT = (
    {
        'id': uuid4(),
        'title': FAKER.cpl_name(),
        'duration': 7200,
        'framerate': 48
    },
    {
        'id': uuid4(),
        'title': FAKER.cpl_name(),
        'duration': 7200,
        'framerate': 48
    },
    {
        'id': uuid4(),
        'title': FAKER.cpl_name(),
        'duration': 7200,
        'framerate': 48
    },
)

def pull_pos_feed():
    return (
        {
            'id': uuid4(),
            'start_stamp': EIGHT_O_CLOCK.timestamp(),
            'end_stamp': (EIGHT_O_CLOCK + timedelta(hours=2)).timestamp()

        }, {
            'id': uuid4(),
            'start_stamp': (EIGHT_O_CLOCK + timedelta(hours=2, minutes=30)).timestamp(),
            'end_stamp': (EIGHT_O_CLOCK + timedelta(hours=4, minutes=30)).timestamp()
        }, {
            'id': uuid4(),
            'start_stamp': (EIGHT_O_CLOCK + timedelta(hours=5)).timestamp(),
            'end_stamp': (EIGHT_O_CLOCK + timedelta(hours=7)).timestamp()
        }
    )

def create_playlists():
    # have the mock content and create "playlists" from it
    return ()


def create_schedules():
    # gather the playlists and put them into the sessions parsed from POS
    # content and schedules are matched up 1:1 ATM;
    # as soon as this isn't the case, we have to match them by title or something...
    return ({'uuid': '', 'name': '', 'start': '', 'end': '', 'playlist': ()})


def send_schedules_to_screen(**kwargs):  # hope it's op_kwargs + context
    data = json.dumps(kwargs['task_instance'].xcom_pull(task_ids='create_schedules'))
    http = HTTPHook(kwargs['method'], http_conn_id=kwargs['http_conn_id'])
    target = "/".join((kwargs['http_conn_id'], kwargs['endpoint']))  # may need better joining
    return http.run(target, data, kwargs['headers'])  # response_check from operator could be better


