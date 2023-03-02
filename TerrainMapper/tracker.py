import json
import math
import sys

import keyboard
import ntplib
import pyperclip
from pynput.keyboard import KeyCode, Listener, Key
import time
from pynput import keyboard as k

#if len(sys.argv) < 2:
#    exit("Specify the planet")

planet = "daymar"

x = []
y = []
z = []

db = open('db.json')
data = json.load(db)

rot_speed = data[planet]["rot_speed"]
rot_adj = 30.7939223  # todo: move to db.json for each planet
radius = data[planet]["radius"]
planet_x = data[planet]["X"]
planet_y = data[planet]["Y"]
planet_z = data[planet]["Z"]


# The key combination to check
COMBINATION = {k.Key.cmd, KeyCode.from_char('f')}

# The currently active modifiers
current = set()

f = open('cave_trace.txt', 'a')

c = ntplib.NTPClient()
response = c.request('europe.pool.ntp.org', version=3)

start_t = 1577836800  # can be hardcoded
def remove_rotation(coords):
    dateDiff = coords["t"] - start_t
    dateDiffDays = abs(dateDiff / (24 * 60 * 60))
    length_of_day_dec = rot_speed * 3600.0 / 86400.0
    julianDate = dateDiffDays
    totalCycles = julianDate / length_of_day_dec
    currentCycleDez = totalCycles % 1
    currentCycleDeg = (currentCycleDez * 360)
    currentCycleAngle = rot_adj + currentCycleDeg
    if (dateDiff < 0):
        currentCycleAngle = 360 - currentCycleAngle
    reversed_angle = 360 - currentCycleAngle
    currentCycleRadians = reversed_angle / 180 * math.pi
    return {
        "x": (coords["x"] * math.cos(currentCycleRadians) - coords["y"] * math.sin(currentCycleRadians)) * -1,
        "y": (coords["x"] * math.sin(currentCycleRadians) + coords["y"] * math.cos(currentCycleRadians)) * -1,
        "z": coords["z"] * -1
    }


def on_press(key):
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            keyboard.press_and_release('enter')
            time.sleep(1)
            keyboard.write("/showlocation", delay=0)
            time.sleep(1)
            keyboard.press_and_release('enter')
            time.sleep(.17)
            cb = pyperclip.paste()
            print("got raw point: " + cb)
            line = "t:" + str(time.time() + response.offset) + " " + cb
            s = line.split(' ')
            del s[1]
            coords_struct = {}
            for idx, i in enumerate(s):
                i = float(i.split(':')[1].strip())
                if idx == 0:
                    coords_struct["t"] = i  # time.time()
                    # coords_struct["t"] = rot_speed * 60 * 60
                elif idx == 1:
                    coords_struct["x"] = planet_x * 1000 - i
                elif idx == 2:
                    coords_struct["y"] = planet_y * 1000 - i
                else:
                    coords_struct["z"] = planet_z * 1000 - i
                    res = remove_rotation(coords_struct)
                    f.write("t:" + str(coords_struct["t"]) + " x:" + str(res["x"]) + " y:" + str(res["y"]) +
                            " z:" + str(res["z"]) + "\n")
                    f.flush()
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