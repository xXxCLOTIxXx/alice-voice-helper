from g4f.client import Client
from g4f.errors import (
    ProviderNotWorkingError,
    ModelNotAllowedError,
    ModelNotSupportedError,
    RateLimitError, RetryProviderError
)


class g4f:
    def __init__(self, model, send_ai_status):
        self.client = Client()
        self.model = model
        self.send_ai_status = send_ai_status
        self.is_stop = False


    def send_response(self, message: str | list):
        if message is None or message == '' or message == ' ':return
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": message}
            ] if isinstance(message, str) else message
        )
        gpt_response = response.choices[0].message.content
        gpt_response=gpt_response.replace("####", "").replace("*", "")
        temp = gpt_response.split("\n\n")
        message = '\n\n'.join(temp[1:] if len(temp)!=1 else temp)
        return message

    def answer(self, message: str | list):
        while True:
            if not self.is_stop:
                self.send_ai_status('думает...')
            else:
                return -10
            try:
                msg = self.send_response(message), 1
                if not self.is_stop:
                    self.send_ai_status('')
                    return msg
            except (
                ProviderNotWorkingError,
                ModelNotAllowedError,
                ModelNotSupportedError,
            ):
                if not self.is_stop:
                    self.send_ai_status('Смена провайдера g4f', 'orange')
                else:
                    return -10
            except RateLimitError:
                if not self.is_stop:
                    return "[G4F] Сервис перегружен. попробуйте позже.", -1
                return -10
            except RetryProviderError:
                if not self.is_stop:
                    self.send_ai_status('Ошибка соединения', 'red')
                return -10
            except Exception as e:
                if not self.is_stop:
                    return f"[G4F] ошибка ({e})", -1
                return -10
    

    def stop(self):
        self.is_stop = True
        self.send_ai_status('Ожидание завершения запроса...', 'orange')