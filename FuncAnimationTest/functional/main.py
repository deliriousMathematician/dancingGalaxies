# in its current state, this simply shows the density heatmap of the galaxy's midplane at various heights above the origin
# going to add text at the bottom right of the plot to indicate height above midplane for each frame
# note that to write the file to disk you need to install ffmpeg from https://ffmpeg.org/ and link the .exe

# imports
import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# variables
vmin = 10**5    # cmap min
vmax = 10**10   # cmap max
z_shift = 0.01  # distance (kpc) to be shifted per frame [breaks if 0.001 or less]
z = 0   # to display height (kpc) above midplane [does not currently do anything]
int = 250   # time (ms) between frames [for plt.show()]

# loading simulation, converting units, and aligning faceon
h = pyn.load('simFiles/run708main.01000')
h.physical_units()
pyn.analysis.angmom.faceon(h)

# creating figure & axes
fig, ax = plt.subplots()

galaxy = pyn.plot.sph.image(h.g, width=16, qty='rho', subplot=ax, cmap=plt.cm.turbo, vmin=vmin, vmax=vmax,
                            title=r'$\rho \text{ at various } z \text{/kpc above midplane}$')

def shift(height):  # shifts the z component height, and adds to the counter
    global z
    h.g['pos'][:, 2] -= height
    z += height
    return None

def update(frame):  # updates animation
    global galaxy
    shift(z_shift)
    galaxy = pyn.plot.sph.image(h.g, width=16, qty='rho', subplot=ax, cmap=plt.cm.turbo, vmin=vmin, vmax=vmax, ret_im=True)
    return galaxy

# animation object
ani = animation.FuncAnimation(fig=fig, func=update, frames=25, interval=int)

plt.show()

# writing to disk using ffmpeg
# matplotlib.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe'  # change path as needed
# writer = animation.FFMpegWriter(fps=5, bitrate=-1)  # -1 automatically assigned the best bit rate
# ani.save('animations/myanimation.mp4', writer=writer)
