import pyautogui as bot


def click(x=None, y=None, clicks=1, interval=0, button=bot.PRIMARY, duration=0.0):
    bot.click(x=x, y=y, clicks=clicks, interval=interval, button=button, duration=duration)


def mouse_move_rel(x, y):
    bot.moveRel(x, y)


def mouse_move_absolute(x, y):
    bot.moveTo(x, y)
