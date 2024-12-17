from requests import ConnectionError
from ...config import initial_prompt

class Brain:
    info = {
        'model': None,
        'type': None,
        'active': False
    }
    worker = None
    busy = False

    history = initial_prompt
    
    def __init__(self, send_ai_status, max_history_length: int = 20):
        self.send_ai_status=send_ai_status
        self.max_history_length = max_history_length

    def set_g4f(self):
        try:
            from .g4f import g4f
            self.worker = g4f('gpt-4', self.send_ai_status)
            self.info['model'] = 'gpt-4'
            self.info['type'] = 'g4f'
            #self.info['active'] = True
        except ConnectionError:
            return '[G4F] Ошибка подключения к интернету.', -1
        except Exception as e:
            return f'[G4F] Ошибка установки ({e}).', -1


    def stop(self):
        if self.busy:
            self.worker.stop()


    def answer(self, message: str):
        if self.worker:
            if self.busy is False:
                self.busy=True
                self.add_message(message)
                result = self.worker.answer(self.history)
                if result and result[1]==1:
                    self.add_message(result[0], 'assistant')
                self.busy = False
                return result
        else:
            return 'Отсуцтвует мыслительная модель', -1 


    def clear_history(self):
        self.history = initial_prompt
    
    def add_message(self, message: str, role: str = 'user'):
        self.history.append({"role": role, "content": message})
        if len(self.history) > self.max_history_length+1:
            self.history.pop(1)