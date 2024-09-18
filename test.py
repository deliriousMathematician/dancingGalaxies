#   - Adjust starting zPos

# Added z_start variable which moves galactic position before starting simulation
# Adjusted dynamic frames calculation to account for non-zero z_start

# Still to do:
# Deal with negative z_shift, z_start, and z_max values
# Test
# Calculate vmin and vmax when at z=0

import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from writers import save_ffmpeg

sim = pyn.load('simFiles/run708main.01000')
pyn.analysis.angmom.faceon(sim)
sim.physical_units()

def z_span(sim, qty="rho", width=16, z_start=0, z_shift=0.01, z_max=0.25, z_rend=True, vmin=None, vmax=None, qtytitle=None,
           show_cbar=True, cmap=plt.cm.turbo, title=None, interval=250, figsize=None, ptext_pos=(0.65, 0.05), **kwargs):

    # Calculating the number of frames dynamically
    frames = int((z_max - z_start) / z_shift) + 1  # +1 to account for frame 0

    # Adjusting starting z
    if z_start != 0:
        sim['pos'][:, 2] -= z_start

    z = z_start    # Defining z for pText

    # Creating Figure and Axes
    if figsize is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = plt.subplots(figsize=figsize)

    # Starting Plot
    galaxy = pyn.plot.sph.image(sim, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

    # Customizing Axes

    # Colorbar
    if show_cbar:
        if qtytitle is None:
            cbar = fig.colorbar(galaxy, ax=ax, label=qty)
        else:
            cbar = fig.colorbar(galaxy, ax=ax, label=qtytitle)

    # Title
    if title is not None:
        axtitle = ax.set_title(title)

    # xyLabels
    xlabel = ax.set_xlabel(f"x/{sim['pos'].units}")
    ylabel = ax.set_ylabel(f"y/{sim['pos'].units}")

    # xyLimits
    xlim = ax.set_xlim(-1 * width / 2, width / 2)
    ylim = ax.set_ylim(-1 * width / 2, width / 2)

    # plotText
    ptext_x, ptext_y = ptext_pos
    if z_rend:
        ptext = fig.text(ptext_x, ptext_y, f'z = {z:.3f} {sim["pos"].units}', transform=ax.transAxes)

    # Setting constant vmin/vmax values to be used for animation
    if (vmin is None) or (vmax is None):
        vmin, vmax = galaxy.get_clim()

    # Defining Update Function
    def update(frame):
        nonlocal galaxy, z
        if frame == 0:  # if initial frame do not shift_z
            return galaxy
        else:
            # shifting z-position of all particles
            sim['pos'][:, 2] -= z_shift

            # Plotting Next Frame
            galaxy.remove()  # Clear the imshow artist to avoid overlapping images
            galaxy = pyn.plot.sph.image(sim, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

            # Updating plotText
            z += z_shift
            ptext.set_text(f'z = {z:.3f} kpc')

            return galaxy

    # Initializing the animation
    ani = animation.FuncAnimation(fig, func=update, frames=frames, interval=interval, **kwargs)

    return ani

ani = z_span(sim.g, qty="rho", z_start = -0.1, z_shift=0.01, title="Rho at various z")

ffmpeg_path = "C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
write_path = "animations\\test.mp4"

save_ffmpeg(ani, ffmpeg_path, write_path, fps=25)