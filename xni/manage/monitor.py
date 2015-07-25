import psutil as ps

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

@app.route('/status.json')
def status():
    response = jsonify(
        cpu_count=ps.cpu_count(),
        cpu_percent=ps.cpu_percent(1, percpu=True)
        )
    return response

def start_monitor(args):
    # TODO: check debug mode
    app.run(debug=True, use_reloader=True)
