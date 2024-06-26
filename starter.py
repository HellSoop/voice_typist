import subprocess as sp
import keyboard
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image


def run_main():
    process = sp.Popen('main.py', shell=True, stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
    run_main.process = process

    for stdout_line in process.stdout:
        if stdout_line in ('Model ready to work!\n', 'Model terminated\n'):
            icon.notify(stdout_line)
            if stdout_line == 'Model ready to work!\n':
                change_running_status.blocked = False

    process.stdout.close()
    run_main.process = None


def start_main_thread():
    if not change_running_status.running:
        Thread(target=run_main, daemon=True).start()
        change_running_status(True)
        icon.notify('Model is starting...')


def change_running_status(status: bool):
    if not change_running_status.blocked:
        change_running_status.running = status
        if status:
            change_running_status.blocked = True


run_main.process = None
change_running_status.blocked = False
change_running_status.running = False

menu = Menu(
    MenuItem('Exit', lambda: icon.stop())
)
img = Image.open(r'logo.jpg')
icon = Icon('Voice Typist', icon=img, menu=menu)

if __name__ == '__main__':
    keyboard.add_hotkey('alt+a', start_main_thread)
    keyboard.add_hotkey('alt+s', change_running_status, args=(False,))
    icon.run()
