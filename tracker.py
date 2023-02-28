import keyboard
from tkinter import Tk
from pynput.keyboard import KeyCode, Listener
import time

f = open("cave_trace.txt", "a")


def on_press(key):
    if key == KeyCode.from_char('f'):
        keyboard.press_and_release('enter')
        time.sleep(1)
        keyboard.write("/showlocation", delay=0)
        time.sleep(1)
        keyboard.press_and_release('enter')
        cb = Tk().clipboard_get()
        f.write("t:" + str(time.time()) + " " + cb + "\n")
        print("saved x-y-z: " + cb)
    if key == KeyCode.from_char('q'):
        f.close()
        exit(0)


with Listener(on_press=on_press) as listener:
    listener.join()
