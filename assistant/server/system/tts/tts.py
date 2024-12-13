import pyttsx3
import threading
from random import randint
from time import sleep

engine = pyttsx3.init() 

tts_active = False
voices = engine.getProperty('voices')


def speak(text):
    global tts_active
    tts_active = True
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 0.7)  # Устанавливаем громкость в 70%
    engine.setProperty('voice', voices[2].id)
    engine.say(text)
    engine.runAndWait()
    tts_active = False




def say(text, send):
    global tts_active
    t = threading.Thread(target=speak, args=(text,))
    t.start()

    while tts_active == True:
        for i in text.split(" "):
            send(len(i*randint(5, 10)))
            sleep(0.05)
            if tts_active == False: break


    send(0)
    t.join()
