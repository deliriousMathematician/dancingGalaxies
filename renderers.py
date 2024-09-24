# imports
import gc
import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from checks import chunk_check, bit_check

def z_span(sim, qty="rho", width=16, z_start=0, z_shift=0.01, z_max=0.25, z_rend=True, vmin=None, vmax=None, qtytitle=None,
           show_cbar=True, cmap=plt.cm.turbo, title=None, interval=250, figsize=None, ptext_pos=(0.65, 0.05), **kwargs):
    """

    Animate SPH images of the given simulation as it varies in the z-axis.

    **Keyword arguments:**

    *sim* : The galaxy object containing the data to visualize.

    *qty* (rho): The name of the array to interpolate

    *width* (16 units): The overall width and height of the plot.
    Units are determined by ``sim['pos']``.

    *z_start* (0): The starting z-position of the animation.
    Units are determined by ``sim['pos']``.

    *z_shift* (0.01 units): The amount to shift in the z-direction per frame.
    Units are determined by ``sim['pos']``.

    *z_max* (0.25 units): Maximum z-distance to cover in the animation.
    Units are determined by ``sim['pos']``.

    *z_rend* (True): Whether the animation renders the current z-position text.

    *vmin* (None): Minimum of the visualization scale. 'None' will choose appropriate value automatically.
    Units are determined by ``sim['qty']``.

    *vmax* (None): Maximum of the visualization scale. 'None' will choose appropriate value automatically.
    Units are determined by ``sim['qty']``.

    *qtytitle* (None): Colorbar quantity title.

    *show_cbar* (True): Whether to plot the colorbar.

    *cmap* (plt.cm.turbo): Colormap to be used.

    *title* (None): Plot Title.

    *interval* (250 ms): Amount of time between the drawing of frames.
    Does not affect playback speed of animation.

    *figsize* (None): Size of the figure on which the plot is rendered. 'None' will choose appropriate value automatically.

    *ptext_pos* (0.65, 0.05): Position of ptext in transAxes coords.

    **Returns:** Animation Object
    """

    # Checking if the dataset is empty in of itself (e.g., no stars or gas in the region) 
    chunk_check(sim[qty])

    # Calculating the number of frames dynamically
    frames = int((z_max - z_start) / z_shift) + 1  # +1 to account for frame 0

    # Creating Figure and Axes
    if figsize is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = plt.subplots(figsize=figsize)

    # Setting constant vmin/vmax values to be used for animation
    if (vmin is None) or (vmax is None):
        galaxy = pyn.plot.sph.image(sim, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)
        vmin, vmax = galaxy.get_clim()
        galaxy.remove()  # Clearing imshow artist

    # Adjusting starting z
    if z_start != 0:
        sim['pos'][:, 2] -= z_start

    z = z_start  # Defining z for pText

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

    # Defining Update Function
    def update(frame):
               
        nonlocal galaxy, z
               
        if frame == 0:  # if initial frame do not shift_z
            return galaxy
        else:
            # shifting z-position of all particles
            sim['pos'][:, 2] -= z_shift

            # Define the z-range for this specific frame
            z_min = z - z_shift / 2
            z_max = z + z_shift / 2

            # Filter the galaxy data for the current frame's z-layer
            current_frame_data = sim['pos'][(sim['pos'][:, 2] >= z_min) & (sim['pos'][:, 2] < z_max)]

            # Checking if there is data in the current frame's slice
            chunk_check(current_frame_data)

            # Plotting the Next Frame
            galaxy.remove()  # Clear the imshow artist to avoid overlapping images
            galaxy = pyn.plot.sph.image(sim, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax,
                                        ret_im=True)

            # Checking for individual NaN Elements
            bit_check(galaxy)

            # Updating plotText
            z += z_shift
            ptext.set_text(f'z = {z:.3f} kpc')

            return galaxy

    # Initializing the animation
    ani = animation.FuncAnimation(fig, func=update, frames=frames, interval=interval, **kwargs)

    return ani


def t_span_sph(snap_dir, snap_name, base_ext_num, num_snaps, qty="rho", width=16, vmin=None, vmax=None, show_cbar=True,
               qtytitle=None, title=None, cmap=plt.cm.turbo, figsize=None, interval=250):
    """

    Animate SPH images of numerous snapshots as they vary in time.

    **Keyword arguments:**

    *snap_dir* :

    *snap_name* :

    *base_ext_num* :

    *num_snaps* :

    *qty* (rho):

    *width* (16 units):

    *vmin* (None):

    *vmax* (None):

    *show_cbar* (True):

    *qtytitle* (None):

    *title* (None):

    *cmap* (plt.cm.turbo):

    *figsize* (None):

    *interval* (250 ms):

    **Returns:** Animation Object
    """

    # Creating Figure and Axes
    if figsize is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = plt.subplots(figsize=figsize)

    # Initializing Starting Frame
    init_snap = pyn.load(f"{snap_dir}/{snap_name}.{int(base_ext_num):05d}")
    init_snap.physical_units()

    pyn.analysis.angmom.faceon(init_snap)

    galaxy = pyn.plot.sph.image(init_snap.g, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

    # Setting constant vmin/vmax values to be used for animation
    if (vmin is None) or (vmax is None):
        vmin, vmax = galaxy.get_clim()

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
    xlabel = ax.set_xlabel(f"x/{init_snap['pos'].units}")
    ylabel = ax.set_ylabel(f"y/{init_snap['pos'].units}")

    del init_snap
    gc.collect()    # Freeing Memory

    # Defining Update Function
    def update(frame):

        nonlocal galaxy

        if frame == 0:  # if initial frame do not remove galaxy
            return galaxy

        else:
            galaxy.remove()     # Clear the imshow artist to avoid overlapping images

            ext_num = int(base_ext_num) + frame     # Extension Number of Current Snap

            current_snap = pyn.load(f"{snap_dir}/{snap_name}.{ext_num:05d}")    # Loading Current Snap
            current_snap.physical_units()   # Converting to Physical Units

            pyn.analysis.angmom.faceon(current_snap)    # Aligning Current Snap [To be made customizable]

            galaxy = pyn.plot.sph.image(current_snap.g, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

            del current_snap    # Freeing Memory
            gc.collect()    # Forcing Garbage Collection

            return galaxy

    ani = animation.FuncAnimation(fig, update, frames=num_snaps, interval=interval)

    return ani


def t_span_stars(snap_dir, snap_name, base_ext_num, num_snaps, width=16, with_dust=False, interval=250):
    """

    Animate star renders of numerous snapshots as they vary in time.

    **Keyword arguments:**

    *snap_dir* :

    *snap_name* :

    *base_ext_num* :

    *num_snaps* :

    *width* (16 units):

    *with_dust* (False):

    *interval* (250 ms):

    **Returns:** Animation Object
    """

    # Creating Figure
    fig = plt.figure()

    # Initializing Starting Frame
    init_snap = pyn.load(f"{snap_dir}/{snap_name}.{int(base_ext_num):05d}")
    init_snap.physical_units()

    pyn.analysis.angmom.faceon(init_snap)

    galaxy = pyn.plot.stars.render(init_snap, width=width, ret_im=True, with_dust=with_dust)

    del init_snap   # Freeing Memory
    gc.collect()    # Forcing Garbage Collection

    # Defining Update Function
    def update(frame):

        nonlocal galaxy

        if frame == 0:  # if initial frame do not remove galaxy
            return galaxy

        else:
            ext_num = int(base_ext_num) + frame     # Extension Number of Current Snap

            current_snap = pyn.load(f"{snap_dir}/{snap_name}.{ext_num:05d}")    # Loading Current Snap
            current_snap.physical_units()   # Converting to Physical Units

            pyn.analysis.angmom.faceon(current_snap)    # Aligning Current Snap [To be made customizable]

            galaxy = pyn.plot.stars.render(current_snap, width=width, ret_im=True, with_dust=with_dust)

            del current_snap    # Freeing Memory
            gc.collect()    # Forcing Garbage Collection

            return galaxy

    ani = animation.FuncAnimation(fig, update, frames=num_snaps, interval=interval)

    return ani
