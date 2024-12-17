
chat_history = []

class Chat:


    def add_message(self, text: str, sender: str = 'user', color: str = 'dark blue'):
        data = {
            'message': text,
            'sender': sender,
            'color': color
        }
        chat_history.append(data)
        return data

    def get_chat_history(self):
        return chat_history
    
    def clear_chat(self):
        global chat_history
        chat_history = []