from .config import port

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from random import randint
from .system.assistant import Assistant
from .config import version

current_radius=0

app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app)

assistant = Assistant(socketio)

@app.route('/')
def index():
    return render_template('index.html', version=version)

@app.route('/settings')
def settings():
    return render_template('settings.html')



@app.route('/version')
def version_info():
    return render_template('version-info.html', version=version)



@app.errorhandler(Exception)
def handle_error(error):
    error_code = getattr(error, 'code', 500) 
    error_message = str(error)
    return render_template('error.html', error_code=error_code, error_message=error_message), error_code



@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Ok.'})

@socketio.on('disconnect')
def handle_disconnect():
    pass

@socketio.on('message')
def handle_message(data):
    assistant.on_message(data)

@socketio.on('command')
def handle_message(data):
    assistant.on_command(data)



def run():
    app.run(port=port)
