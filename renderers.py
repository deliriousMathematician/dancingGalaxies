# imports
import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def z_span(sim, qty="rho", width=16, z_shift=0.01, z_max=0.25, z_rend=True, vmin=None, vmax=None, qtytitle=None,
           show_cbar=True, cmap=plt.cm.turbo, title=None, interval=250, figsize=None, ptext_pos=(0.65, 0.05), **kwargs):
    """

    Animate SPH images of the given simulation as it varies in the z-axis.

    **Keyword arguments:**

    *sim* : The galaxy object containing the data to visualize.

    *qty* (rho): The name of the array to interpolate

    *width* (16 units): The overall width and height of the plot.
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

    # defining z [TO BE MADE ADJUSTABLE]
    z = 0

    # Calculating the number of frames dynamically
    frames = int(z_max / z_shift) + 1  # +1 to account for frame 0

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
