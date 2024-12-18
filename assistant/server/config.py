"""
Made by Xsarz

GitHub [https://github.com/xXxCLOTIxXx]
Discord [https://discord.gg/GtpUnsHHT4]
YouTube  [https://www.youtube.com/@Xsarzy]
"""

from . import settings

version = "1.0"

port = 5000
server_url = f"http://127.0.0.1:{port}"
title = f'Голосовой ассистент {settings.settings.get("other", {}).get("names", ["ERROR"]).split(",")[0]}'
size = (500, 650)