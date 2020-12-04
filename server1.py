import flask
import time

app = flask.Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/status')
def status():
    current_time = time.time()
    my_time = time.ctime(current_time)
    print(my_time)
    status = {
        'status': True,
        'name': 'P5Q server',
        'time': my_time
    }
    return status

status()


app.run()
