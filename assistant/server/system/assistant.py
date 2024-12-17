from .stt.stt import stt
from .commands.cmd import CommandManager
from threading import Thread
from .out.out import Out
from .storage.chat import Chat
from .brain.brain import Brain
from ..config import names
from time import sleep
from .utils import clear_names
from os import system

_stt = stt()

class Assistant:    

	def __init__(self, socketio):
		self.socketio=socketio
		self.l = Thread(target=_stt.listen, args=(self.on_voice_message,))
		self.l.daemon = True
		self.l.start()
		self.chat = Chat()
		self.out = Out(socketio, self.chat)
		self.cmd = CommandManager(self.out)
		self.brain = Brain(self.send_ai_status)
		
		status = self.brain.set_g4f()
		if status:
			self.out.out(status[0], status[1])
		
		self.ai_status_info = {
			'text': '',
			'color': ''
		}

		Thread(target=self.status_loop, daemon=True).start()

	def status_loop(self):
		while True:
			self.socketio.emit('ai_status', self.ai_status_info)
			sleep(0.3)



	def send_ai_status(self, text, color = '#666'):
		self.ai_status_info = {"text":text, "color":color}



	def on_voice_message(self, text):
		if text in ['', ' ', None]:return
		if self.execute_base_commands(text):return
		c = self.cmd.detect_command(text=text)
		if c:
			self.out.log(text, 'user', '#1e3a8a')
			self.cmd.handle_command(c)
			return
		if self.brain.info.get("active") and not self.brain.busy and not self.out.tts.tts_active:
			self.out.log(text, 'user', '#1e3a8a')
			msg = self.brain.answer(text)
			if not msg:return
			self.out.out(msg[0], msg[1])

		


	def on_message(self, data: dict | str):
		text = data.get("text") if isinstance(data, dict) else data
		self.out.log(text, 'user', '#1e3a8a')
		if self.execute_base_commands(text):return
		c = self.cmd.detect_command(text=text)
		if c:
			self.cmd.handle_command(c)
			return
		if self.brain.info.get("active") and not self.brain.busy and not self.out.tts.tts_active:
			msg = self.brain.answer(text)
			if not msg:return
			self.out.out(msg[0], msg[1])

	def on_command(self, data: dict | str):
		text = data.get("keyword") if isinstance(data, dict) else data
		self.out.log('[cmd] '+text, 'user', 'gray')
		self.cmd.handle_command(text)




	def execute_base_commands(self, text: str) -> bool:
		ts = text
		text = clear_names(text)
		if text in ('молча', 'тихо', 'молчи') and self.brain.info['active'] == True:
			if self.brain.info['active'] == False:return True
			self.brain.info['active'] = False
			self.out.out("Поддержка диалога отключена")
			return True
		if text == 'говори':
			if self.brain.info['active'] == True:return True
			self.brain.info['active'] = True
			self.out.out("Поддержка диалога включена")
			return True
		if text == 'стоп' and (self.out.tts.tts_active or self.brain.busy):
			self.out.log(ts, 'user', '#1e3a8a')
			self.out.tts.stop()
			self.brain.stop()
			return True
		if text in ("перезагрузи компьютер", "перезагрузить компьютер"):
			system("shutdown /r")

		return False

