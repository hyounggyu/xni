import psutil as ps

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

@app.route('/status.json')
def status():
    cpu = ps.cpu_percent(1, percpu=True)
    mem = ps.virtual_memory()
    mem_dict = dict(mem.__dict__)
    response = jsonify(
        cpu_percents=[{'cpu_id': i, 'cpu_percent': load} for i, load in enumerate(cpu)],
        mem=mem_dict
        )
    return response

def start_monitor(args):
    port = 5059 if args.port == None else args.port
    # TODO: check debug mode
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)
