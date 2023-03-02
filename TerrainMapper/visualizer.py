import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    exit("Specify a file or filepath to render")

file = sys.argv[1]

x = []
y = []
z = []

with open(file) as f:
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
                x.append(i)
            elif idx == 2:
                y.append(i)
            else:
                z.append(i)

    f.close()

fig = plt.figure()
fig.canvas.manager.set_window_title("Maulwurf -> TerrainMapper")
ax = plt.axes(projection='3d')
ax.set_title("tracking " + file)
N = 5  # some number > 1 that stretches z axis as you desire
#ax.set_box_aspect((25, 10, 10)) # xy aspect ratio is 1:1, but stretches z axis
plt.xlabel("X")
plt.ylabel("Y")
plt.plot(x, y, z, color="red", marker='o')
plt.show()
