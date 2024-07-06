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
        if stdout_line == 'Model is ready to work!':
            change_running_status.blocked = False
            create_short_notification(stdout_line)
        elif stdout_line == 'Model terminated':
            create_short_notification('Model is closing...', 0.7)

    else:
        process.stdout.close()
        run_main.process = None
        change_running_status(False)
        create_short_notification('Model terminated')


def start_main_thread() -> None:
    if not change_running_status.running:
        change_running_status(True)
        Thread(target=run_main, daemon=True).start()
        create_short_notification('Model is starting...', 0.7)


def change_running_status(status: bool) -> None:
    if not change_running_status.blocked:
        change_running_status.running = status
        if status:
            change_running_status.blocked = True


run_main.process = None
change_running_status.blocked = False
change_running_status.running = False


# icon functions
def notify_short(text: str, timeout: int | float = 1.1) -> None:
    icon.notify(text, title='Voice Typist')
    sleep(timeout)
    icon.remove_notification()


def create_short_notification(text: str, timeout: int | float = 1.1) -> None:
    Thread(target=notify_short, args=(text, timeout), daemon=True).start()


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
    keyboard.add_hotkey('alt+a', start_main_thread, suppress=True)
    icon.run()
