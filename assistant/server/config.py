"""
Made by Xsarz

GitHub [https://github.com/xXxCLOTIxXx]
Discord [https://discord.gg/GtpUnsHHT4]
YouTube  [https://www.youtube.com/@Xsarzy]
"""

version = "0.349.15.12"

names = (
    "ева", 'ев'
)

port = 5000
server_url = f"http://127.0.0.1:{port}"
title = f"Голосовой ассистент {names[0]}"
size = (500, 650)


names = (
    "ева", 'ев'
)

gender = "девушка"


initial_prompt = [
    {
        "role": "system",
        "content": f"Ты голосовой ассистент-{gender} {names[0]}. Ты дружелюбная, интеллигентная и немного с юмором. Твои ответы всегда полезны, четки и соответствуют запросу, но ты можешь добавить немного легкости и тепла в общении."
    }
]
