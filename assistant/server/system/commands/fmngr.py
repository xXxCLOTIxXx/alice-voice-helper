import os
import subprocess
import platform

def open_file(file_path):
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux
            subprocess.run(["xdg-open", file_path])
        return True
    except Exception as e:
        return e



def launch_file(file_path):
    try:
        subprocess.run(file_path, check=True)
        return True
    except Exception as e:
        return e