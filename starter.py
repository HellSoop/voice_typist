import sys
import subprocess as sp
import keyboard
from time import sleep
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image


# model functions
def run_main() -> None:
    process = sp.Popen([sys.executable, '-u', 'main.py'], stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
    run_main.process = process

    for stdout_line in process.stdout:
        stdout_line = stdout_line.strip()
        if stdout_line == 'Model ready to work!':
            change_running_status.blocked = False
            create_short_notification(stdout_line)

    else:
        process.stdout.close()
        run_main.process = None
        change_running_status(False)
        create_short_notification('Model terminated')


def start_main_thread() -> None:
    if not change_running_status.running:
        Thread(target=run_main, daemon=True).start()
        change_running_status(True)
        create_short_notification('Model is starting...')


def change_running_status(status: bool) -> None:
    if not change_running_status.blocked:
        change_running_status.running = status
        if status:
            change_running_status.blocked = True


run_main.process = None
change_running_status.blocked = False
change_running_status.running = False


# icon functions
def create_short_notification(text: str) -> None:
    icon.notify(text)
    sleep(1.2)
    icon.remove_notification()


def close_app():
    if run_main.process is not None:
        run_main.process.terminate()
    icon.stop()


# create icon
menu = Menu(
    MenuItem('Exit', close_app),
)
img = Image.open(r'logo.jpg')
icon = Icon('Voice Typist', icon=img, menu=menu)

if __name__ == '__main__':
    keyboard.add_hotkey('alt+a', start_main_thread)
    icon.run()
