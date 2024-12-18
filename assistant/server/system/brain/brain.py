from requests import ConnectionError
from ... import settings
from .chatgpt import chatGPT

class Brain:
    info = {
        'model': None,
        'type': None,
        'active': False
    }
    worker = None
    busy = False

    history = []
    initial_prompt = settings.settings.get("other", settings.default_settings.get("other")).get("initial_prompt", "Ты голосовой ассистент")
    
    def __init__(self, send_ai_status, max_history_length: int = 20):
        self.send_ai_status=send_ai_status
        self.max_history_length = max_history_length
        

    def set_g4f(self):
        try:
            self.send_ai_status("G4F starting...", 'orange')
            from .g4f import g4f
            self.worker = g4f('gpt-4', self.send_ai_status)
            self.info['model'] = 'gpt-4'
            self.info['type'] = 'g4f'
            #self.info['active'] = True
            self.busy = False
            self.send_ai_status("")
        except ConnectionError:
            return '[G4F] Ошибка подключения к интернету.', -1
        except Exception as e:
            return f'[G4F] Ошибка установки ({e}).', -1

    def set_gpt(self, token):
        try:
            if token in (None, '', " "):
                return f'[GPT] Токен не указан.', -1
            self.send_ai_status("GPT starting...", 'orange')
            self.worker = chatGPT(token, self.send_ai_status)
            self.info['model'] = '?'
            self.info['type'] = 'chatgpt'
            #self.info['active'] = True
            self.busy = False
            self.send_ai_status("")
        except ConnectionError:
            return '[GPT] Ошибка подключения к интернету.', -1
        except Exception as e:
            return f'[GPT] Ошибка установки ({e}).', -1


    def stop(self):
        if self.busy and self.worker:
            self.worker.stop()
            if self.info.get("type") != 'g4f':
                self.busy = False



    def answer(self, message: str):
        if self.worker:
            if self.busy is False:
                self.busy=True
                self.add_message(message)
                result = self.worker.answer(self.history)
                if result ==  -10:
                    if self.info['type']=='g4f':
                        self.send_ai_status('')
                    return
                if result and result[1]==1:
                    self.add_message(result[0], 'assistant')
                self.busy = False
                return result
        else:
            return 'Отсуцтвует мыслительная модель', -1 


    def clear_history(self):
        self.history = []
    
    def add_message(self, message: str, role: str = 'user'):
        self.history.insert(0, {"role": "system", "content": self.initial_prompt})
        self.history.append({"role": role, "content": message})
        if len(self.history) > self.max_history_length + 1:
            self.history.pop(1)


    def update(self):
        m = settings.settings.get("dialog_model", settings.default_settings.get("dialog_model"))
        self.initial_prompt = settings.settings.get("other", settings.default_settings.get("other")).get("initial_prompt", "Ты голосовой ассистент")
        if self.info["active"] == True and m.get("dialog_mode", False) == False:
            self.stop()
        self.info["active"] = m.get("dialog_mode", False)
        if m.get("model") != self.info.get("type") or self.worker is None:
            if self.worker:
                self.worker.stop()
                del self.worker
                self.worker = None
            if m.get("model") == "g4f":
                return self.set_g4f()
            if m.get("model") == "chatgpt":
                return self.set_gpt(m.get("token"))
            self.worker = None
            return 'Отсуцтвует мыслительная модель', -1