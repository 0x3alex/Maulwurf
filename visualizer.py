import json
import math
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    exit("Specify a name of a planet")

x = []
y = []
z = []

db = open('db.json')
data = json.load(db)

planet = sys.argv[1].lower()
rot_speed = data[planet]["rot_speed"]
radius = data[planet]["radius"]


def remove_rotation(coords):
    w = rot_speed / radius
    wt = w * coords["t"]
    return {
        "x": coords["x"] * (math.cos(-1 * wt) - math.sin(-1 * wt)),
        "y": coords["y"] * (math.cos(-1 * wt) + math.sin(-1 * wt)),
        "z": coords["z"]
    }


with open('cave_trace.txt') as f:
    lines = f.readlines()
    for line in lines:
        s = line.split(' ')
        del s[1]
        current_timestamp = None
        coords_struct = {}
        for idx, i in enumerate(s):
            i = float(i.split(':')[1].strip())
            if idx == 0:
                coords_struct["t"] = rot_speed * 60 * 60
            elif idx == 1:
                T = coords_struct["t"] % coords_struct["t"]
                coords_struct["x"] = i / 1000000
            elif idx == 2:
                T = coords_struct["t"] % coords_struct["t"]

                coords_struct["y"] = i / 1000000
            else:
                T = coords_struct["t"] % coords_struct["t"]
                coords_struct["z"] = i / 1000000
                res = remove_rotation(coords_struct)
                x.append(res["x"])
                y.append(res["y"])
                z.append(res["z"])

    f.close()

fig = plt.figure()
fig.canvas.manager.set_window_title(planet)
ax = plt.axes(projection='3d')
fx = np.array(x)
fy = np.array(z)
fz = np.array(y)
plt.plot(fx, fy, fz, color="red")
plt.show()
