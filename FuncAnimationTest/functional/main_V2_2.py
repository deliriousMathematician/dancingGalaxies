# Imports
import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import os

# Variables
vmin = 10**5    # Colormap minimum
vmax = 10**10   # Colormap maximum
z_shift = 0.01  # Distance (kpc) to be shifted per frame [avoid values <= 0.001]
z_max = 0.25    # Maximum z-distance to cover in the animation (kpc)
interval = 250  # Time (ms) between frames
colorbar = True # To toggle colorbar on/off...can add user option later on

# Calculating the number of frames dynamically
frames = int(z_max / z_shift)

# Loading simulation, converting units, and aligning face-on
try:
    h = pyn.load('run708main.01000')
except FileNotFoundError:
    raise FileNotFoundError("Simulation file not found. Check your file path.")
h.physical_units()
pyn.analysis.angmom.faceon(h)

# Creating the figure & axes
fig, ax = plt.subplots(figsize=(8, 8))
if colorbar:
    cbar = fig.colorbar(galaxy, ax=ax)

# Defining the starting plot (latex was bugging)
# plt.rc('text', usetex=True)
galaxy = pyn.plot.sph.image(
    h.g, 
    width=16, 
    qty='rho', 
    subplot=ax, 
    cmap=plt.cm.turbo, 
    vmin=vmin, 
    vmax=vmax,
    title=r'$\rho \, \mathrm{at\ various} \, z / \mathrm{kpc\ above\ midplane}$'
)
# or title=r'$\rho \, \text{at various} \, z / \text{kpc above midplane}$'

text_height = fig.text(0.75, 0.05, 'z = 0.00 kpc', transform=ax.transAxes)  # Display starting height

# Functions (Modified them to try something...)

def shift_z(height):
    
    """Shift the galaxy slice in the z direction."""
    
    h.g['pos'][:, 2] -= height
    return None

def update(frame):
    
    """Update the animation for each frame."""
    
    global galaxy, z
    shift_z(z_shift)
    z += z_shift
    
    # Update plot
    ax.clear()  # Clear the axes to avoid overlapping images
    galaxy = pyn.plot.sph.image(
        h.g, 
        width=16, 
        qty='rho', 
        subplot=ax, 
        cmap=plt.cm.turbo, 
        vmin=vmin, 
        vmax=vmax, 
        ret_im=True
    )
    
    # Updating the colorbar if enabled
    if colorbar:
        cbar.update_normal(galaxy)

    # Updating the height text
    text_height.set_text(f'z = {z:.2f} kpc')
    
    return galaxy

# Initializing the animation
ani = animation.FuncAnimation(fig, func=update, frames=frames, interval=interval, repeat=False)

# Writing to disk using ffmpeg
ffmpeg_path = 'C:\\Users\\User\\Desktop\\BSc.M&P\\Extra\\Astro\\ffmpeg.exe'
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError("FFmpeg not found. Check your ffmpeg installation path.")

matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path  # Adjust path
writer = animation.FFMpegWriter(fps=5, bitrate=-1)  # -1 for automatic best bitrate
ani.save('animations/myanimation2.mp4', writer=writer)

# Cleanup and closing plot to free memory
plt.close(fig)

# Known issues:
# - Must ensure z_shift and z_max are appropriately chosen for your data
# - Must check file paths for the simulation file and FFmpeg installation cause it...it pains me
