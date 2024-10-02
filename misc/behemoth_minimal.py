# Project BEHEMOTH V2 - Balancing the Evolution of Halos, Environments and Massive Objects: Tracking History
# karl c
# A reduced minimalistic version of the basic functionality we may need.
# What remains to be done is to integrate it with the other code in some ways and refine the output movie whichever way is deemed best.
# There do remain some unused remanants of previous code versions from other py files in this code.
# I will place some other new functions in a different file soon.

# Imports

import pynbody as pyn
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import os
import gc  # garbage collection

# Stars

def star_ages (sim):
    
    stars = sim.stars
    current_time = sim.properties['time'].in_units('Gyr')
    star_ages = current_time - stars['tform'].in_units('Gyr')
    y_stars = stars[star_ages < 1]
    i_stars = stars[(star_ages > 1) & (star_ages < 5)]
    o_stars = stars[star_ages > 5]
    
    return y_stars, i_stars, o_stars

def plot_star_render(snapshot, ax, width=50):
    
    ax.clear()
    galaxy = pyn.plot.stars.render(snapshot.s, width=width, axes=ax, ret_im=True)
    
    return galaxy

# Creating a 2D sph plot of the gas component of a snapshot.

def plot_gas_sph(snapshot, ax, qty="rho", width=50, vmin=None, vmax=None, cmap='turbo'):
    
    ax.clear()
    galaxy = pyn.plot.sph.image(snapshot.g, qty=qty, width=width, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)
    
    return galaxy

# Plotting a 2D Snapshot of all galactic components (experimental).

def plot_all_components(snapshot, ax, overlay_vel=False):
    
    ax.clear()
    
    ax.scatter(snapshot.stars['x'], snapshot.stars['y'], s=0.1, c='red', label='Stars', alpha=0.5)
    ax.scatter(snapshot.gas['x'], snapshot.gas['y'], s=0.1, c='green', label='Gas', alpha=0.5)
    ax.scatter(snapshot.dm['x'], snapshot.dm['y'], s=0.1, c='blue', label='Dark Matter', alpha=0.5)

    if overlay_vel:
        ax.quiver(snapshot.stars['x'], snapshot.stars['y'], snapshot.stars['vx'], snapshot.stars['vy'], color='yellow', scale=100, alpha=0.5)

    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.legend()

# Loading and processing eash snapshots one by one.

def snap_loader(snap_dir, snap_number):
    
    snap = pyn.load(f"{snap_dir}/run670hTDiffMetalCoolF10HRHC.{snap_number:05d}")
    snap.physical_units()
    pyn.analysis.angmom.faceon(snap)
    
    return snap

# Saving the frames of the simulation (with a progress bar).

def save_frames(snap_dir, output_dir='frames', num_snaps=50, qty="rho", width=50, vmin=None, vmax=None, overlay_vel=False, all_components=False, stars = False):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fig, ax = plt.subplots(figsize=(6, 6))
    
    print("Progress bar of simulation files being loaded, analysed and saved as frames: ")
    
    for i in tqdm(range(num_snaps+1)):
        snap_number = 1700 + i
        snapshot = snap_loader(snap_dir, snap_number)
        
        if all_components:
            plot_all_components(snapshot, ax, overlay_vel)
            
        elif stars:
            plot_star_render(snapshot, ax, width=width)
            
        else:
            plot_gas_sph(snapshot, ax, qty=qty, width=width, vmin=vmin, vmax=vmax)

        plt.savefig(f'{output_dir}/frame_{i:03d}.png')
        
        del snapshot  # Freeing up memory after the plotting
        gc.collect()  # Forcing the garbage collection

    plt.close()

# Creating the animation using Matplotlib's FuncAnimation.

def create_animation(snap_dir, num_snaps=50, qty="rho", width=50, vmin=None, vmax=None, save_to='galaxy_simulation.mp4'):
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    print("Creating the animation...")
    
    def animate(i):
        
        snap_number = 1700 + i
        snapshot = snap_loader(snap_dir, snap_number)
        plot_gas_sph(snapshot, ax, qty=qty, width=width, vmin=vmin, vmax=vmax)
        
        del snapshot  # Freeing up memory after the plotting
        gc.collect()  # Forcing the garbage collection

    ani = FuncAnimation(fig, animate, frames=num_snaps, interval=100)
    
    plt.close()
    
    return ani

# Saving the animation using FFmpeg.

def save_ffmpeg(ani, ffmpeg_path, write_path, fps=5, bitrate=-1, dpi=200):
    
    matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path
    writer = animation.FFMpegWriter(fps=fps, bitrate=bitrate)
    ani.save(write_path, writer=writer, dpi=dpi)
    plt.close()

# Main function: creates the frames and animation.

def main(snap_dir, ffmpeg_path, num_snaps=50, output_dir='frames', create_video=True, view_3d=False, overlay_vel=False, z_span_mode=False):
    
    # Generating the frames.
    save_frames(snap_dir, output_dir=output_dir, num_snaps=num_snaps, overlay_vel=overlay_vel)

    # Creating a video from the frames (some remenants which are uneeded but can act as link in future for newer code versions).
    if create_video:
        
        if z_span_mode:
            
            sim = pyn.load(f'{snap_dir}/snapshot_000')
            # ani = z_span(sim.g, qty="rho", z_shift=0.001, title="Rho at various z")
            
            # save_ffmpeg(ani, ffmpeg_path, f'{output_dir}/z_span.mp4', fps=25)
            
        else:
            
            animation = create_animation(snap_dir, num_snaps=num_snaps, save_to=f'{output_dir}/galaxy_simulation.mp4')
            save_ffmpeg(animation, ffmpeg_path, f'{output_dir}/galaxy_simulation.mp4', fps=25)


# Usage
if __name__ == '__main__':
    
    snapshot_directory = r'C:\Users\User\Desktop\BSc.M&P\Extra\Astro\DA_BEHEMOTH\snapshots'
    ffmpeg_dir = r"C:\Users\User\Desktop\BSc.M&P\Extra\Astro\ffmpeg_folder\bin\ffmpeg.exe"
    main(snapshot_directory, ffmpeg_dir)
