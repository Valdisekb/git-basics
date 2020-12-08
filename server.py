

import flask
import time
from flask import request, abort

app = flask.Flask(__name__)

db = []


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/status')
def status():
    current_time = time.time()
    my_time = time.ctime(current_time)
    status = {
        'status': True,
        'name': 'P5Q server',
        'time': my_time
    }
    return status


@app.route('/send', methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)
    name = request.json['name']
    text = request.json['text']

    if not (isinstance(name, str)
            and isinstance(text, str)
            and name
            and text):
        return abort(400)

    new_message = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    db.append(new_message)

    return {'ok': True}


@app.route('/messages')
def get_messages():
    try:
        after = float(request.args.get('after', 0))
    except ValueError:
        return abort(400)

    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)
    return {'messages': messages}


app.run()
