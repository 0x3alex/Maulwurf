import datetime
import json
import math
import time

import matplotlib.pyplot as plt
import sys
from pathlib import Path
from datetime import timezone
import ntplib

if len(sys.argv) < 2:
    exit("Specify a file or filepath to render")
if len(sys.argv) < 3:
    exit("Specify a name of a planet")

file = sys.argv[1]
if not Path(file).is_file():
    exit("Not a valid file")

planet = sys.argv[2].lower()


x = []
y = []
z = []

db = open('db.json')
data = json.load(db)

rot_speed = data[planet]["rot_speed"]
rot_adj = 30.5679523  # todo: move to db.json for each planet
radius = data[planet]["radius"]
planet_x = data[planet]["X"]
planet_y = data[planet]["Y"]
planet_z = data[planet]["Z"]

'''dt = datetime.datetime(2020, 1, 1)
start_t = dt.replace(tzinfo=timezone.utc).timestamp()
c = ntplib.NTPClient()
response = c.request('europe.pool.ntp.org', version=3)'''

start_t = 1577836800  # can be hardcoded

log = open("output_log.txt", 'a')

#start_t = response.tx_time
def remove_rotation(coords):
        log.write("---new coords----\n")
        log.write("coords " + str(coords) + "\n")
        dateDiff = coords["t"] - start_t
        log.write("dateDiff " + str(dateDiff) + "\n")
        dateDiffDays = abs(dateDiff / (24*60*60))
        log.write("dateDiffDays " + str(dateDiffDays) + "\n")
        length_of_day_dec = rot_speed * 3600.0 / 86400.0
        log.write("length_of_day_dec " + str(length_of_day_dec) + "\n")
        julianDate = dateDiffDays
        log.write("julianDate " + str(julianDate) + "\n")
        totalCycles = julianDate / length_of_day_dec
        log.write("totalCycles " + str(totalCycles) + "\n")
        currentCycleDez = totalCycles % 1
        log.write("currentCycleDez " + str(currentCycleDez) + "\n")
        currentCycleDeg = (currentCycleDez * 360)
        log.write("currentCycleDeg " + str(currentCycleDeg) + "\n")
        currentCycleAngle = rot_adj + currentCycleDeg
        if (dateDiff < 0):
            currentCycleAngle = 360 - currentCycleAngle
        log.write("currentCycleAngle " + str(currentCycleAngle) + "\n")
        reversed_angle = 360 - currentCycleAngle
        log.write("reversed_angle " + str(reversed_angle) + "\n")
        currentCycleRadians = reversed_angle / 180 * math.pi
        log.write("currentCycleRadians " + str(currentCycleRadians) + "\n")
        return {
            "x": (coords["x"] * math.cos(currentCycleRadians) - coords["y"] * math.sin(currentCycleRadians)) * -1,
            "y": (coords["x"] * math.sin(currentCycleRadians) + coords["y"] * math.cos(currentCycleRadians)) * -1,
            "z": coords["z"] * -1
        }


with open(file) as f:
    log.write("parsing " + file + "\n")
    lines = f.readlines()
    for line in lines:
        s = line.split(' ')
        del s[1]
        coords_struct = {}
        for idx, i in enumerate(s):
            i = float(i.split(':')[1].strip())
            if idx == 0:

                coords_struct["t"] = i # time.time()
                #coords_struct["t"] = rot_speed * 60 * 60
            elif idx == 1:
                coords_struct["x"] = planet_x * 1000 - i
            elif idx == 2:
                coords_struct["y"] = planet_y * 1000 - i
            else:
                coords_struct["z"] = planet_z * 1000 - i
                #print(coords_struct)
                res = remove_rotation(coords_struct)
                log.write("final " + str(res) + "\n")
                x.append(res["x"])
                y.append(res["y"])
                z.append(res["z"])
    log.close()
    f.close()
print(x)
print(y)
print(z)
fig = plt.figure()
fig.canvas.manager.set_window_title("On: " + planet + " tracking: " + file)
ax = plt.axes(projection='3d')
N = 5  # some number > 1 that stretches z axis as you desire
#ax.set_box_aspect((25, 10, 10)) # xy aspect ratio is 1:1, but stretches z axis
plt.xlabel("X")
plt.ylabel("Y")
plt.plot(x, y, z, color="red", marker='o')
plt.show()
