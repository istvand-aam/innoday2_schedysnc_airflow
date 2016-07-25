import json
import os

from flask import Flask, request, jsonify, render_template


app = Flask(__name__, template_folder='.')
SCHEDULES_FILENAME = 'schedules.json'
SCHEDULES = []


def _cache_schedules():
    with open(SCHEDULES_FILENAME, 'w') as schedules_file:
        json.dump(SCHEDULES, schedules_file)


def _load_schedules_cache():
    global SCHEDULES
    if not os.path.exists(SCHEDULES_FILENAME):
        _cache_schedules()
    with open(SCHEDULES_FILENAME) as schedules_file:
        SCHEDULES = json.load(schedules_file)


# load the cache
_load_schedules_cache()


@app.route('/api/schedules', methods=('POST',))
def save_schedule():
    schedule_data = request.json
    SCHEDULES.append(schedule_data)
    _cache_schedules()
    return jsonify(message='SUCCESS', schedule=schedule_data)


@app.route('/api/schedules')
def get_schedules():
    return jsonify(schedules=SCHEDULES)


@app.route('/api/schedules/clear')
def clear_schedules():
    global SCHEDULES
    SCHEDULES = []
    _cache_schedules()
    return jsonify(message='SUCCESS')


@app.route('/')
def index():
    return render_template('schedules.html', schedules=SCHEDULES)
