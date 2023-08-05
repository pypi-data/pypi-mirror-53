from time import sleep

from pynput.keyboard import Controller

keyboard = Controller()


def keyboard_type(string):
    global keyboard
    keyboard.type(string)


def keyboard_press_and_release(keys):
    global keyboard
    if type(keys) == list:
        for key in keys:
            keyboard.press(key)
        for key in reversed(keys):
            keyboard.release(key)
    else:
        keyboard.press(keys)
        keyboard.release(keys)


def keyboard_press(keys):
    global keyboard
    if type(keys) == list:
        for key in keys:
            keyboard.press(key)
    else:
        keyboard.press(keys)


def keyboard_release(keys):
    global keyboard
    if type(keys) == list:
        for key in keys:
            keyboard.release(key)
    else:
        keyboard.release(keys)
