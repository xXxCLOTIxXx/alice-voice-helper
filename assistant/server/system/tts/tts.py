import pyttsx3
from ..utils import split_space

engine = pyttsx3.init() 

class TTS:
    stop_flag = False
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 0.7)
    engine.setProperty('voice', voices[2].id)
    tts_active = False


    def speak(self, text):
        if self.tts_active: 
            return
        
        def _speak():
            global engine
            self.tts_active = True
            words = split_space(text)
            for word in words:
                if self.stop_flag:
                    break
                engine.say(word)
                engine.runAndWait()
            
            self.tts_active = False
            self.stop_flag = False
        
        _speak()


    def stop(self):
        global engine
        if self.tts_active:
            self.stop_flag = True