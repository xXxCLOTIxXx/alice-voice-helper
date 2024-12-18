import webbrowser
import json
import os
from random import choice

from ..out.out import Out
from .fmngr import open_file, launch_file
from ..utils import clear_names

base_commands = [
    {'keyword': 'открой ютуб',
     'args': 
        {
            'type': 'open_page',
            'url': 'https://www.youtube.com/@Xsarzy'
        }
    },
    {
        "keyword": "тест русского",
        "args": {
            "type": "answer_msg",
            "answer_msg": "Привет мир. как твои дела?"
        }
    },
    {
        "keyword": "тест английского",
        "args": {
            "type": "answer_msg",
            "answer_msg": "Hello world. how are you?"
        }
    },
    {
        "keyword": "открой проводник",
        "args": {
            "type": "console_command",
            "command": "start explorer"
        }
    },
    {
        "keyword": "перезагрузи компьютер",
        "args": {
            "type": "console_command",
            "command": "shutdown /r /f /t 0"
        }
    }

]


ok_messgaes = [
    "Выполняю", "Секунду", "Готово", 'Один момент'
]


def get_command_by_keyword(commands, keyword):
    for cmd in commands:
        if cmd['keyword'].lower() == keyword.lower():
            return cmd
    return None

class CommandManager:
    def __init__(self, out: Out, json_file='commands.json'):
        self.json_file = json_file
        if not os.path.exists(self.json_file):
            self.save_commands(base_commands)
        self.out=out



    def get_commands(self):
        return self.load_commands()

    def add_command(self, keyword, args):
        commands = self.load_commands()
        if not any(cmd['keyword'] == keyword for cmd in commands):
            commands.append({"keyword": keyword, "args": args})
            self.save_commands(commands)

    def delete_command(self, keyword):
        commands = self.load_commands()
        commands = [cmd for cmd in commands if cmd['keyword'] != keyword]
        self.save_commands(commands)

    def load_commands(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            self.save_commands(base_commands)
            return base_commands

    def save_commands(self, commands):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(commands, f, ensure_ascii=False, indent=4)




    def handle_command(self, keyword):
        keyword = keyword.lower()
        commands = self.get_commands()
        command = get_command_by_keyword(commands, keyword)
        if not command:
            self.out.out("Команда не найдена.")
            return
        args = command.get("args")
        log_msg = ""
        match args.get("type"):
            case 'open_page':
                result = webbrowser.open(args.get("url"))
                if not result: log_msg =f"Не удалось открыть ссылку '{args.get('url')}'"
            case 'open_file':
                result = open_file(args.get('path'))
                if result != True: log_msg =f"Не удалось открыть файл '{args.get('path')}' ({result})"
            case 'run_file':
                result = launch_file(args.get('path'))
                if result != True: log_msg =f"Не удалось запустить программу '{args.get('path')}' ({result})"
            case 'answer_msg':
                self.out.out(args.get("answer_msg"))
                return
            case 'console_command':
                if args.get("command"):
                    os.system(args.get("command"))
                return  True
        

        if result is True:
            self.out.out(choice(ok_messgaes))
        else:
            self.out.out("Не удалось выполнить команду.", 0)
            self.out.out(log_msg, -1)

    

    def detect_command(self, text: str) -> str | None:
        text = text.strip().lower()
        commands = self.get_commands()

        text = clear_names(text)
        for command in commands:
            keyword = command.get('keyword', '').lower()
            if text.startswith(keyword):
                return keyword

        return None