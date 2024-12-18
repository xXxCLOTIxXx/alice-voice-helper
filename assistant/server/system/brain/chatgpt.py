import openai as oa



class chatGPT:
    def __init__(self, token: str, send_ai_status):
        self.client=oa.OpenAI(api_key=token)
        self.model="gpt-3.5-turbo"
        self.send_ai_status = send_ai_status
        self.is_stop = False
    

    def send_response(self, message: str | list):
        if message is None or message == '' or message == ' ':return

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": message}
                ] if isinstance(message, str) else message
            )
            gpt_response = (ck.choices[0].delta.content or "" for ck in response)
            gpt_response=gpt_response.replace("####", "").replace("*", "")
            temp = gpt_response.split("\n\n")
            return '\n\n'.join(temp[1:] if len(temp)!=1 else temp), 1
        except Exception as e:
            return f"[GPT] {e}", -1

    def answer(self, message: str | list):
        if not self.is_stop:self.send_ai_status('думает...')
        else:
            self.send_ai_status('')
            return
        try:
            msg = self.send_response(message)
            if not self.is_stop:
                self.send_ai_status('')
                return msg
        except Exception as e:
            if not self.is_stop:
                self.send_ai_status('')
                return f"[GPT] ошибка ({e})", -1
            self.send_ai_status('')






    def stop(self):
        self.is_stop = True
        self.send_ai_status('Ожидание завершения запроса...', 'orange')