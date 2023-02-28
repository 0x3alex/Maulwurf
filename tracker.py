import keyboard
import pyperclip
from pynput.keyboard import KeyCode, Listener, Key
import time
from pynput import keyboard as k

# The key combination to check
COMBINATION = {k.Key.alt_gr, KeyCode.from_char('f')}

# The currently active modifiers
current = set()

f = open('cave_trace.txt', 'a')

def on_press(key):
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            keyboard.press_and_release('enter')
            time.sleep(1)
            keyboard.write("/showlocation", delay=0)
            time.sleep(1)
            keyboard.press_and_release('enter')
            cb = pyperclip.paste()
            print(cb)
            f.flush()
            f.write("t:" + str(time.time()) + " " + cb + "\n")
            print("saved x-y-z: ")
    if key == KeyCode.from_char('q'):
        f.close()
        listener.stop()
        exit(0)


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


with k.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

'''def on_press(key):
    if key in combination:
        print(key)
        currently_pressed.add(key)

    if currently_pressed == combination:
        is_pressed = True
        print('pressed!')
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
'''