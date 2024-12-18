from .config import port

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from random import randint
from .system.assistant import Assistant
from . import settings as s
from .config import version
import webbrowser
from threading import Thread
from json import dumps
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

app = Flask(__name__, static_url_path="/static")
socketio = SocketIO(app)

assistant = Assistant(socketio)

@app.route('/')
def index():
    return render_template('index.html', version=version)

@app.route('/settings')
def settings():
    return render_template('settings.html')



@app.route('/commands')
def commands_page():
    return render_template('commands.html')

@app.route('/chat')
def chat_page():
    return render_template('chat-page.html')

@app.route('/info')
def info_page():
    return render_template('info-page.html', version=version)


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

@socketio.on('get_commands')
def handle_get_commands():
    commands = assistant.cmd.get_commands()
    emit('commands_list', commands)

@socketio.on('execute_command')
def handle_execute_command(data):
    keyword = data.get("keyword")
    assistant.on_command(keyword)

@socketio.on('add_command')
def handle_add_command(data):
    keyword = data.get('keyword')
    args = data.get('args')
    assistant.cmd.add_command(keyword, args)
    emit('commands_list', assistant.cmd.get_commands(), broadcast=True)

@socketio.on('delete_command')
def handle_delete_command(data):
    keyword = data.get('keyword')
    assistant.cmd.delete_command(keyword)
    emit('commands_list', assistant.cmd.get_commands(), broadcast=True)


@socketio.on('send_message')
def handle_send_message(data):
    Thread(target=assistant.on_message, args=(data.get("message"),), daemon=True).start()

@socketio.on('get_history')
def handle_get_history():
    emit('history', assistant.chat.get_chat_history())

@socketio.on('chat_clear')
def handle_get_history():
    assistant.chat.clear_chat()
    assistant.brain.clear_history()



@socketio.on('open_link')
def open_link(data):
    url = data.get('url')
    if url:webbrowser.open(url)


@socketio.on('reset_settings')
def handle_connect():
    s.reset_to_defaults()
    assistant.on_settings_update()
    emit('settings_data', dumps(s.settings))


@socketio.on('get_settings_data')
def handle_connect():
    emit('settings_data', dumps(s.settings))


@socketio.on('update_settings')
def handle_connect(data):
    s.save_settings(data)
    assistant.on_settings_update()
    emit('settings_data', dumps(s.settings))

@socketio.on("get_models")
def on_update_models(data):
    emit('update_models', {
        "models":
            assistant.out.tts.get_voice_models(data['type']),
        "current":
            s.settings.get("synthesis", {}).get("voice") if s.settings.get("synthesis", {}).get("type") == data['type'] else None
    })

def select_file():
    #QApplication(sys.argv)
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    if file_dialog.exec_():
        selected_file = file_dialog.selectedFiles()[0]
        return selected_file
    return None

@socketio.on('select_file')
def handle_select_file():
    try:
        file_path = select_file()
        emit('file_selected', {'file_path': file_path if file_path else None}, broadcast=True)
    except Exception as e:
        emit('file_selected_error', {'message': str(e)}, broadcast=True)





def run():
    app.run(port=port)
