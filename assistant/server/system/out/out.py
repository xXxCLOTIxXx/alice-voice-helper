from ..tts.tts import TTS

import threading
from random import randint
from time import sleep
from flask_socketio import  SocketIO

class Out:
    tts = TTS()

    def __init__(self, socketio: SocketIO, chat):
        self.socketio=socketio
        self.chat = chat


    def update_canvas(self, radius: int, color: str = None):
        self.socketio.emit('canvas_update', {'radius': radius, 'color': color})
    
    def say(self, text):
        t = threading.Thread(target=self.tts.speak, args=(text,))
        t.start()

        while self.tts.tts_active == True:
            for i in text.split(" "):
                self.update_canvas(len(i*randint(5, 10)))
                sleep(0.05)
                if self.tts.tts_active == False: break


        self.update_canvas(0)
        t.join()


    def out(self, text: str, type = 1):
        match type:
            case 1:
                self.log(text)
                self.say(text)
            case 0:
               self.say(text)
            case -1:
                self.log(text, 'system', 'red')
    

    def log(self, message: str, type: int = 'bot', color = 'rgb(74, 34, 123)'):
        data = self.chat.add_message(message, type, color)
        self.socketio.emit('new_message', data)