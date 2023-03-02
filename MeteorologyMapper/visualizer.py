import random

from matplotlib import cm
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def split_by_value(l, splitter):
    lower = []
    higher = []
    for i in l:
        if i <= splitter:
            lower.append(i)
        else:
            higher.append(i)
    return lower, higher


lookUp = {
    1: "No Weather",
    2: "Rain",
    3: "Storm"
}

n = 100

timeOfDay = []
weather = []
temps = []
area = "test data"
for i in range(0, 10):
    n = random.randint(1, 23)
    timeOfDay.append(n)

for i in range(0, 10):
    n = random.randint(1, 3)
    weather.append(n)

for i in range(0, 10):
    n = random.randint(50, 150)
    temps.append(n)

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

cmp = ListedColormap(['blue', 'red'])

img = ax.scatter(timeOfDay, weather, temps, marker='s',
                 s=50, cmap=cmp, c=temps)

for x, y, z in zip(timeOfDay, weather, temps):
    ax.text(x, y, z + 2, "{} - {}°C".format(lookUp[y], z))

ax.set_title("mapping of weather data in '" + area + "'")

ax.set_xlabel('time\n(unix)')

ax.set_ylabel('weather\n(number)')

ax.set_zlabel('temperature')
fig.canvas.manager.set_window_title("Maulwurf -> MeteorologyMapper")
# displaying plot
plt.show()
