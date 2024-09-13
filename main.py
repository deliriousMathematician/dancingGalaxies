"""
Title: Astrophysics Galactic Animation Creator Program
Version: 1.2.3
Last Updated: 13/09/2024
"""

# To Do;

#   - Create functionality to choose what to plot, or at least dictate how one can change the code to do so and generally create/refine the User Interface
#   - Add comments as necessary.
#   - Test for issues and resolve as possible. (See at the end for a list thereof)
#   - Add width and cmap to user interface
#   - Remove z from user interface (we don't have functionality to adjust starting z at the moment. It's only current use is the counter on the plot)
#   - ...

# --------------------------------------------------------------------------------------------------------------------------------------------------------- #

# Imports.

# Importing the pynbody package to handle the galactic simulation.
import pynbody as pyn
# Importing the matplotlib library to handle the plotting and animation.
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Importing the os module to interact with the device OS.
import os

# Initializing the needed Variables.

# Keeping these as comments to serve as default test values.
# vmin = 10 ** 5  # Colormap minimum
# vmax = 10 ** 10  # Colormap maximum
# z_shift = 0.01  # Distance (kpc) to be shifted per frame [avoid values <= 0.001]
# z_max = 0.25  # Maximum z-distance to cover in the animation (kpc)
# interval = 250  # Time (ms) between frames
# z = 0
width = 16  # x-y span
cmap = plt.cm.turbo # colormap

# Function to encapsulate the user inputs (each wrapped in a while loop so program doesn't need to be restarted in case of mistake.).
# Refine further as you please... (should probably change the names of variables inside and outside, or find how to refine this to reduce redundancy, via the use of global)
def get_user_inputs():
    
    # vmin (getting exponent which must be positive)
    while True:
        try:
            vmin_exp = int(input("\nEnter a positive exponent for the colormap minimum (vmin) (E.g., 5 for 10^5): "))
            if vmin_exp < 0:
                raise ValueError("vmin_exp must be a positive number")
            vmin = 10 ** vmin_exp
            break
        
        except ValueError as e:
            print(f"Invalid input for vmin: {e}. Please try again.")
    
    # vmax (getting exponent which must be greater than that of vmin)
    while True:
        try:
            vmax_exp = int(input("\nEnter the exponent for the colormap maximum (vmax) (E.g., 10 for 10^10): "))
            vmax = 10 ** vmax_exp
            if vmax <= vmin:
                raise ValueError("vmax must be greater than vmin")
            break
        
        except ValueError as e:
            print(f"Invalid input for vmax: {e}. Please try again.")
    
    # z_shift (set at a minimum limit of 0.001)
    while True:
        try:
            z_shift = float(input("\nEnter the distance along z to be shifted per frame (z_shift) (E.g., 0.01): "))
            if z_shift <= 0.001:
                raise ValueError("z_shift must be greater than 0.001")
            break
        
        except ValueError as e:
            print(f"Invalid input for z_shift: {e}. Please try again.")
    
    # z_max (must be positive)
    while True:
        try:
            z_max = float(input("\nEnter the maximum z-distance (z_max) to be covered in the animation (E.g., 0.25): "))
            if z_max <= 0:
                raise ValueError("z_max must be a positive number")
            break
        
        except ValueError as e:
            print(f"Invalid input for z_max: {e}. Please try again.")
    
    # interval (must be positive)
    while True:
        try:
            interval = int(input("\nEnter the time (in ms) between frames (i.e., the interval) (E.g., 250): "))
            if interval <= 0:
                raise ValueError("interval must be a positive number")
            break
        
        except ValueError as e:
            print(f"Invalid input for interval: {e}. Please try again.")

    # colorbar (adjusted so that it is not case or space sensitive)
    while True:

        colorbar_input = input("\nToggle the colorbar on/off (Enter True/False): ").strip().lower()

        if colorbar_input == 'true':
            colorbar = True
            break

        elif colorbar_input == 'false':
            colorbar = False
            break

        else:
            print("Invalid input for the colorbar. Must be either 'True' or 'False'. Please try again.")
    
    # z (set so it cannot be negative)
    while True:
        try:
            z = float(input("\nEnter the starting z-coordinate (E.g., 0): "))
            if z < 0:
                raise ValueError("z must be a non-negative number")
            break
        
        except ValueError as e:
            print(f"Invalid input for z: {e}. Please try again.")
    
    # Return the values if all inputs are valid.
    return vmin, vmax, z_shift, z_max, interval, colorbar, z

# Calling the function (not an efficient method of doing this, will fix later)
user_values = get_user_inputs()
vmin = user_values[0]  # Colormap minimum
vmax = user_values[1]  # Colormap maximum
z_shift = user_values[2]  # Distance (kpc) to be shifted per frame [avoid values <= 0.001]
z_max = user_values[3]  # Maximum z-distance to cover in the animation (kpc)
interval = user_values[4]  # Time (ms) between frames
colorbar = user_values[5] # To toggle colorbar on/off...can add user option later on
z = user_values[6] # Starting z

# 'Confirming' the values.
if user_values:
    print(f"\nThe following are the received input values: \nvmin: {vmin}, \nvmax: {vmax}, \nz_shift: {z_shift}, \nz_max: {z_max}, \ninterval: {interval}, \ncolorbar: {colorbar}, \nz: z")

# Calculating the number of frames dynamically
frames = int(z_max / z_shift)

# Loading Simulation
sim = input("Enter Simulation Path: ")  # User input
# sim = "simFiles/run708main.01000"

try:
    h = pyn.load(sim)
except FileNotFoundError:
    raise FileNotFoundError("Simulation file not found. Check your file path.")

# Converting units and aligning face-on
h.physical_units()
pyn.analysis.angmom.faceon(h)

# Creating Figure and Axes
fig, ax = plt.subplots()

# Starting Plot
galaxy = pyn.plot.sph.image(h.g, width=width, qty='rho', vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

# Customizing Plot
if colorbar:
    cBar = fig.colorbar(galaxy, ax=ax, label="cbar")
title = ax.set_title("test")
xLabel = ax.set_xlabel("x/kpc")
yLabel = ax.set_ylabel("y/kpc")
xLim = ax.set_xlim(-1 * width/2, width/2)
yLim = ax.set_ylim(-1 * width/2, width/2)

# Plot Text
pText = fig.text(0.75, 0.05, f'z = {z:.2f} kpc', transform=ax.transAxes)

# Animation Functions


def shift_z(height):

    """Shift the galaxy slice in the z direction."""

    h.g['pos'][:, 2] -= height
    return None


def update(frame):

    """Update the animation for each frame."""

    global galaxy, z, width, vmin, vmax, cmap

    # Shift particles
    shift_z(z_shift)
    z += z_shift

    # Update plot

    galaxy.remove()  # Clear the imshow artist to avoid overlapping images
    galaxy = pyn.plot.sph.image(h.g, width=width, qty='rho', vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

    # Updating the height text
    pText.set_text(f'z = {z:.2f} kpc')

    return galaxy


# Initializing the animation
ani = animation.FuncAnimation(fig, func=update, frames=frames, interval=interval, repeat=False)

# Writing to disk using ffmpeg
# 'C:\\Users\\User\\...\\ffmpeg_folder\\bin\\ffmpeg.exe'

ffmpeg_path = input("Enter the ffmpeg file path: ") # User input
# ffmpeg_path = "C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError("FFmpeg not found. Check your ffmpeg installation path.")

matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path  # Set path as source
writer = animation.FFMpegWriter(fps=5, bitrate=-1)  # -1 for automatic best bitrate
ani.save('animations/animation1.mp4', writer=writer)

# Cleanup and closing plot to free memory
plt.close(fig)

# Known issues:
# - Must ensure z_shift and z_max are appropriately chosen for your data
# - Must check file paths for the simulation file and FFmpeg installation cause it...it pains me
