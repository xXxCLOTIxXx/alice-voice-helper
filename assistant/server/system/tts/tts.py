from .pyttsx import pyTTSx
from .g_tts import GTTS
from .silerotts import SileroTTS

from ... import settings

class TTS:


    def __init__(self):
        self.worker = pyTTSx()
        self.update()

    def speak(self, text):
        if not settings.settings.get("input_output", {}).get("speak", False):return
        if self.worker:
            self.worker.speak(text)


    def stop(self):
        if self.worker:self.worker.stop()


    def update(self):
        voice_name=settings.settings.get("synthesis", {}).get("voice", None)
        volume = settings.settings.get("input_output", {}).get("volume", 0.5)
        vtype = settings.settings.get("synthesis", {}).get("type", None)
        if vtype == "pyttsx3":
            if self.worker:
                self.worker.stop()
                del self.worker
            self.worker = pyTTSx()
        elif vtype == "silero":
            if self.worker:
                self.worker.stop()
                del self.worker
            self.worker = SileroTTS()
        elif vtype == "gtts":
            if self.worker:
                self.worker.stop()
                del self.worker
            self.worker = GTTS()

        if isinstance(self.worker, pyTTSx):
            self.worker.update(
                float(volume),
                voice_name=voice_name,
            )
        if isinstance(self.worker, GTTS):
            self.worker.update(float(volume))
        if isinstance(self.worker, SileroTTS):
            self.worker.update(voice_name, float(volume))


    def get_voice_models(self, type):
        if type == 'pyttsx3':
            return pyTTSx.get_voices()
        if type == 'silero':
            return SileroTTS.get_voices()

    @property
    def tts_active(self):
        if self.worker:return self.worker.tts_active
        else: False