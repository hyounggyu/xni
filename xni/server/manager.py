from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

def start():
    print('Start XNI manager...')
    app.run()
