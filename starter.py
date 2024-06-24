import subprocess as sp
import keyboard
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image


def start_model():
    if not change_running_status.running:
        model_thread = Thread(target=sp.run, args=('main.py', ), kwargs={'shell': True}, daemon=True)
        model_thread.start()
        change_running_status(True)
        icon.notify('Model started')


def change_running_status(status: bool):
    change_running_status.running = status


change_running_status.running = False
menu = Menu(
    MenuItem('Exit', lambda: icon.stop())
)
img = Image.open(r'logo.jpg')
icon = Icon('Voice Typist', icon=img, menu=menu)

if __name__ == '__main__':
    keyboard.add_hotkey('alt+a', start_model)
    keyboard.add_hotkey('alt+s', change_running_status, args=(False,))
    icon.run()
