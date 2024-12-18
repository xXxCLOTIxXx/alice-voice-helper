import os
import shutil
import colorama
import site
colorama.init()

"""
Made by xsarz for voice assistant alice project!
"""

def get_site_packages_path():
    paths = site.getsitepackages()
    for path in paths:
        if 'site-packages' in path.lower():
            return path
    return


RES_DIR = 'server'
BUILD_DIR = 'build'
IGNORE = ['.py', '.pyc', '__pycache__']
ICON_PATH = "server/static/media/icon.png"
V='0.217'

SPKG_PATH = get_site_packages_path()
PY_REQUIREMENTS = [
'pyqt5',
'flask',
'vosk',
'PyQtWebEngine',
'flask_socketio',
'sounddevice',
'pyttsx3',
'g4f',
'gtts',
'pygame',
'torch',
'omegaconf',
'num2words',
'openai',
'numpy',


'pyinstaller',
'pillow'
]
INCLUDE_MODULES = [
    'vosk',
    'engineio',
    'torch',
    'omegaconf',
    'antlr4'
]


def ignore(file_name) -> bool:
    return any(file_name.endswith(ignore) for ignore in IGNORE) or file_name in IGNORE


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_empty_dirs(directory):
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        for dirname in dirnames:
            dir_full_path = os.path.join(dirpath, dirname)
            if not os.listdir(dir_full_path):
                os.rmdir(dir_full_path)
                print(f"{colorama.Fore.GREEN}Empty folder deleted: {dir_full_path}{colorama.Fore.RESET}")


def copy_files(src_dir, dest_dir, ignoring: bool = True):
    if not os.path.exists(src_dir):
        print(f"{colorama.Fore.RED}Source res dir '{src_dir}' not found.{colorama.Fore.RESET}")
        return

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if ignoring:
            if ignore(item):
                print(f"{colorama.Fore.YELLOW}Ignore: {src_path}{colorama.Fore.RESET}")
                continue

        if os.path.isdir(src_path):
            copy_files(src_path, dest_path, ignoring)
        else:
            shutil.copy2(src_path, dest_path)
            print(f"{colorama.Fore.GREEN}Copied: {src_path} -> {dest_path}{colorama.Fore.RESET}")


def create_exe():
    os.system(f"pyinstaller -i {ICON_PATH} --distpath {BUILD_DIR}/dist --workpath {BUILD_DIR}/buid --noconsole main.py")


def add_include_modules():
    for module in INCLUDE_MODULES:
        copy_files(f"{SPKG_PATH}\\{module}", f"{BUILD_DIR}/_internal/{module}", ignoring=False)

def run():
    os.system("clear || cls")
    print(f"{colorama.Fore.LIGHTBLUE_EX}Alice Build Script V{V}{colorama.Fore.RESET}")
    print(f"[{colorama.Fore.BLACK}BUILD DIR: {colorama.Back.BLUE}{BUILD_DIR}{colorama.Back.RESET}{colorama.Fore.RESET}] [{colorama.Fore.BLACK}RES DIR: {colorama.Back.GREEN}{RES_DIR}{colorama.Back.RESET}{colorama.Fore.RESET}]")
    print(f"{colorama.Fore.BLACK}Python requirements: {colorama.Fore.LIGHTMAGENTA_EX}{colorama.Fore.LIGHTYELLOW_EX}{PY_REQUIREMENTS}{colorama.Fore.RESET}")
    print(f"{colorama.Fore.BLACK}Ignore files: {colorama.Fore.LIGHTMAGENTA_EX}{colorama.Fore.LIGHTYELLOW_EX}{IGNORE}{colorama.Fore.RESET}")
    print(f"{colorama.Fore.BLACK}Installing libs...{colorama.Fore.RESET}")
    os.system(f"pip install {' '.join(PY_REQUIREMENTS)}")
    if os.path.exists(BUILD_DIR):shutil.rmtree(f"{BUILD_DIR}")
    print(f"{colorama.Fore.BLACK}Creating exe...{colorama.Fore.RESET}")
    create_exe()
    print(f"{colorama.Fore.BLACK}Мoving collected files...{colorama.Fore.RESET}")
    copy_files(f"{BUILD_DIR}/dist/main", f"{BUILD_DIR}")
    shutil.rmtree(f"{BUILD_DIR}/buid")
    shutil.rmtree(f"{BUILD_DIR}/dist")
    print(f"{colorama.Fore.BLACK}Adding modules for inclusion in the program folder...{colorama.Fore.RESET}")
    add_include_modules()
    print(f"{colorama.Fore.BLACK}Copying resource files...{colorama.Fore.RESET}")
    for _path in (F"{BUILD_DIR}/{RES_DIR}", F"{BUILD_DIR}/_internal/{RES_DIR}"):
        copy_files(RES_DIR, _path)
        remove_empty_dirs(_path)
    delete_file("main.spec")
    shutil.rmtree(f"{BUILD_DIR}/_internal/{RES_DIR}/system")
    for dir in ('static', 'templates'):
        shutil.rmtree(f"{BUILD_DIR}/{RES_DIR}/{dir}")
    print(f"{colorama.Fore.GREEN}Programm save in {BUILD_DIR}{colorama.Fore.RESET}")



if __name__ == "__main__":
    run()