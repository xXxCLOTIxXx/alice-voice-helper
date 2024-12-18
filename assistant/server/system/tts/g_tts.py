import os
import threading
from gtts import gTTS
import pygame
import tempfile
from time import sleep

class GTTS:
    volume = 0.5
    def __init__(self, lang="ru"):
        self.lang = lang
        self._is_speaking = False
        self._stop_flag = threading.Event()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)


    @property
    def tts_active(self):
        return self._is_speaking

    def speak(self, text):
        if self._is_speaking:
            return

        self._is_speaking = True
        self._stop_flag.clear()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file.close()

        try:
            tts = gTTS(text=text, lang=self.lang, slow=False)
            tts.save(temp_file.name)

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

            thread = threading.Thread(target=_play_audio, daemon=True)
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


    def update(self, volume: float):
        if volume:self.volume = volume