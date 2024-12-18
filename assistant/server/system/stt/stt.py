

import vosk
import sounddevice as sd
import queue
from json import loads
from threading import Thread
from ... import settings
from time import sleep

#stt
stt_model: str = "server/system/stt/model"
samplerate: int = 16000
device: int = 1

class stt:

	vosk_model = vosk.Model(stt_model)
	q = queue.Queue()
	active = True


	def q_callback(self, indata, frames, time, status):
		self.q.put(bytes(indata))


	def listen(self, callback):
		with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16', channels=1, callback=self.q_callback):
			rec = vosk.KaldiRecognizer(self.vosk_model, samplerate)
			while self.active:
				data = self.q.get()
				if rec.AcceptWaveform(data):
					if settings.settings.get("input_output", {}).get("listen", False) is False:
						continue
					Thread(target=callback, args=(loads(rec.Result())["text"],), daemon=True).start()
		

	def input_devices(self):
		devices = sd.query_devices()
		input_devices = [d for d in devices if d['max_input_channels'] > 0]
		return input_devices



	def update(self):
		pass