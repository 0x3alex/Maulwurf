import json
import random
import sys
import time

from matplotlib import cm
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def parse(list,axis,planet,json_obj):
    f = json.load(open("db.json"))
    if axis == "timestamp":
        list.append(time.mktime(time.strptime(json_obj["date"] + " " + json_obj["time"], '%Y-%m-%d %H:%M')))
    elif axis == "temperature":
        list.append(float(json_obj[axis]))
    else:

        val = json_obj[axis]
        list.append(float(f[planet][axis][val]))


if len(sys.argv) < 8:
    exit("visualizer.py <file> <planet> <location> <value_for_x_axis> "
         "<value_for_y_axis> <value_for_z_axis> <color_reference_axis>")

file = "test_data.json"
planet = sys.argv[2]
location = sys.argv[3]

if sys.argv[4] == sys.argv[5] or sys.argv[4] == sys.argv[6] or sys.argv[5] == sys.argv[6]:
    print("Multiple axis can not have the same value to represent")

valid_axis_values = ["timestamp", "temperature"]
with open("db.json") as db:
    data = json.load(db)
    for obj in data[planet]:
        valid_axis_values.append(obj)
    db.close()


x_idx = sys.argv[4] if sys.argv[4] in valid_axis_values else exit("Not valid 4")
y_idx = sys.argv[5] if sys.argv[5] in valid_axis_values else exit("Not valid 5")
z_idx = sys.argv[6] if sys.argv[6] in valid_axis_values else exit("Not valid 6")
color_reference = "" if sys.argv[7] == "x" or sys.argv[7] == "y" or sys.argv[7] == "z" \
                              else exit("Not valid color reference - x y or z")

x = []
y = []
z = []

with open(file) as f:
    data = json.load(f)
    for obj in data["data"]:
        parse(x, x_idx, planet, obj)
        parse(y, y_idx, planet, obj)
        parse(z, z_idx, planet, obj)

    f.close()

if color_reference == "x":
    color_reference = x
elif color_reference == "y":
    color_reference = y
else:
    color_reference = z

print(x)
print(y)
print(z)


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

cmp = ListedColormap(['blue', 'red'])

img = ax.scatter(x, y, z,marker='s',
                 s=50, cmap=cmp, c=color_reference)

# for x, y, z in zip(x, y, z):
#    ax.text(x, y, z + 2, "{} - {}°C".format(lookUp[y], z))

ax.set_title(location)

ax.set_xlabel(x_idx)

ax.set_ylabel(y_idx)

ax.set_zlabel(z_idx)
fig.canvas.manager.set_window_title("Maulwurf -> MeteorologyMapper")
# displaying plot
plt.show()
