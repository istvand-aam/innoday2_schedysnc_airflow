from flask import Flask, request, jsonify, render_template


app = Flask(__name__, template_folder='.')
SCHEDULES = []


@app.route('/api/schedules', methods=('POST',))
def save_schedule():
    schedule_data = request.json
    SCHEDULES.append(schedule_data)
    return jsonify(message='SUCCESS', schedule=schedule_data)


@app.route('/api/schedules')
def get_schedules():
    return jsonify(schedules=SCHEDULES)


@app.route('/')
def index():
    return render_template('schedules.html', schedules=SCHEDULES)

