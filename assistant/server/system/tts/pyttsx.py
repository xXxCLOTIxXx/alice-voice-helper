import pyttsx3
import pygame
import tempfile
import os
from time import sleep
from threading import Thread, Event

engine = pyttsx3.init()

_voices = {}

class pyTTSx:
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 180)
    _is_speaking = False
    volume = 0.5

    def __init__(self):
        for voice in self.voices:
            _voices[str(voice.name)] = voice.id
        self._stop_flag = Event()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

    @property
    def tts_active(self):
        return self._is_speaking


    
    def get_voices():
        return list(_voices.keys())


    def speak(self, text):
        if self._is_speaking:
            return

        self._is_speaking = True
        self._stop_flag.clear()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.close()

        try:
            engine.save_to_file(text, temp_file.name)
            engine.runAndWait()

            def _play_audio():
                try:
                    pygame.mixer.music.load(temp_file.name)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() and not self._stop_flag.is_set():
                        sleep(0.1)
                    if self._stop_flag.is_set():
                        pygame.mixer.music.stop()
                except Exception as e:
                    pass
                finally:
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    self._is_speaking = False
                    try:
                        os.remove(temp_file.name)
                    except PermissionError:
                        pass
                    pygame.mixer.init()
                    pygame.mixer.music.set_volume(self.volume)

            thread = Thread(target=_play_audio, daemon=True)
            thread.start()
        except Exception:
            self._is_speaking = False
            try:
                os.remove(temp_file.name)
            except PermissionError:
                pass









    def stop(self):
        if self._is_speaking:
            self._stop_flag.set()

    def update(self, volume: float = None, voice_id=None, voice_name=None):
        if volume:
            self.volume = volume
            engine.setProperty('volume', volume)
        if voice_id:
            engine.setProperty('voice', voice_id)
        elif voice_name:
            engine.setProperty('voice', _voices.get(voice_name))