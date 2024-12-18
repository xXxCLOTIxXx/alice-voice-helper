import torch
import pygame
import tempfile
import os
from time import sleep
from threading import Thread, Event
import numpy as np
import wave
from ..utils import text_to_words
import sys
import os

# Перенаправить stderr в пустой поток
sys.stderr = open(os.devnull, 'w')


# Настройки
language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
put_accent = True
put_yo = True
device = torch.device('cpu')  # cpu / gpu
pygame.mixer.init()

# Загрузка модели
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)

class SileroTTS:
    def __init__(self):
        self._is_speaking = False
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        self._stop_flag = Event()
        self.speaker = 'kseniya'

    @property
    def tts_active(self):
        return self._is_speaking

    @staticmethod
    def get_voices():
        return ['aidar', 'baya', 'kseniya', 'xenia']


    def speak(self, text):
        if self._is_speaking:return
        self._is_speaking = True
        self._stop_flag.clear()
        try:

            audio_tensor = model.apply_tts(
                text=text_to_words(text) + "...",
                speaker=self.speaker,
                sample_rate=sample_rate,
                put_accent=True,
                put_yo=True
            )
            audio_numpy = audio_tensor.cpu().numpy()
            audio_numpy = audio_numpy / np.max(np.abs(audio_numpy))
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_file.close()
            
            with wave.open(temp_file.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                audio_data = (audio_numpy * 32767).astype(np.int16)
                wf.writeframes(audio_data.tobytes())


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

    def update(self, speaker: str, volume: float = None):
        if volume:
            self.volume = volume
            pygame.mixer.music.set_volume(volume)
        if speaker:
            self.speaker=speaker
