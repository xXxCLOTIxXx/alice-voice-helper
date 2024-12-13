import webbrowser


commands: dict = {
    "включи музыку": lambda: webbrowser.open("https://www.youtube.com/watch?v=jfKfPfyJRdk"),
}



def handle_command(command: str):
    if command in commands:
        commands[command]()
        return True
    return False