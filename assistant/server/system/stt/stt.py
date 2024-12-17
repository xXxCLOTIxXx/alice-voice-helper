

import vosk
import sounddevice as sd
import queue
from sys import stderr
from json import loads
from threading import Thread

#stt
stt_model: str = "server/system/stt/model/vosk-model"
samplerate: int = 16000
device: int = 1

class stt:

	vosk_model = vosk.Model(stt_model)
	q = queue.Queue()


	def q_callback(self, indata, frames, time, status):
		self.q.put(bytes(indata))


	def listen(self, callback):
		with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16', channels=1, callback=self.q_callback):
			rec = vosk.KaldiRecognizer(self.vosk_model, samplerate)
			while True:
				data = self.q.get()
				if rec.AcceptWaveform(data):
					Thread(target=callback, args=(loads(rec.Result())["text"],), daemon=True).start()
