from .tts.tts import say
from .stt.stt import stt
from .commands.cmd import handle_command

_stt = stt()
from threading import Thread



class Assistant:
    

    def __init__(self, socketio):
        self.socketio=socketio
        self.l = Thread(target=_stt.listen, args=(self.on_voice_message,))
        self.l.start()


    def on_voice_message(self, text):
        handle_command(text)


    def on_message(self, data):
        #say(data.get("text"), self.update_canvas)
        handle_command(data.get("text"))

    def on_command(self, data):
        pass


    def update_canvas(self, radius: int, color: str = None):
        self.socketio.emit('canvas_update', {'radius': radius, 'color': color})