import json
import os

class Settings:
    settings = {}
    def __init__(self, file_path="settings.json"):
        self.file_path = file_path
        self.default_settings = {
            'synthesis':
                {'type': 'gtts', 'voice': None},
            'input_output':
                {'volume': '50', 'speak': True, 'listen': True},
            'dialog_model': 
                {'model': 'g4f', 'token': None, 'dialog_mode': False},
            'other':
                {'names': 'ева, ев', 'initial_prompt': 'Ты голосовой ассистент-девушка Ева. Ты дружелюбная, интеллигентная и немного с юмором. Твои ответы всегда полезны, четки и соответствуют запросу, но ты можешь добавить немного легкости и тепла в общении.'}
            }
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        else:
            self.save_settings(self.default_settings)
            return self.default_settings.copy()

    def save_settings(self, new_settings=None):
        if new_settings:
            self.settings.update(new_settings)
        with open(self.file_path, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key):
        return self.settings.get(key, None)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def reset_to_defaults(self):
        self.settings = self.default_settings.copy()
        self.save_settings()