

import vosk
import sounddevice as sd
import queue
from sys import stderr
from json import loads

#stt
stt_model: str = "server/system/stt/model/vosk-model-small-ru-0.22"
samplerate: int = 16000
device: int = 1

class stt:

	vosk_model = vosk.Model(stt_model)
	q = queue.Queue()


	def q_callback(self, indata, frames, time, status):
		if status:
			print(status, file=stderr)
		self.q.put(bytes(indata))


	def listen(self, callback):
		with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16', channels=1, callback=self.q_callback):
			rec = vosk.KaldiRecognizer(self.vosk_model, samplerate)
			while True:
				data = self.q.get()
				if rec.AcceptWaveform(data):
					callback(loads(rec.Result())["text"])