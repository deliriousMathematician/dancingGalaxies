# imports
import pynbody as pyn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def chunk_check (data):
    # Checking if the supplied data chunk (be it the galactic dataset of a slice of) is empty (e.g., no stars or gas in the region) 
    # (For the extreme case of total absence of data.)
    if len(data) == 0:
        print(f"No data available for selected quantity in the selected region.")
        plt.figure()
        plt.text(0.5, 0.5, 'No data in this region', horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.show()
        return None  

def bit_check (galaxy): 
    # Converting the current frame image into a NumPy array for pixel inspection to do an image data check specifcally.
    img_data = galaxy.get_array()

    # Checking for empty elements in the current slice (e.g., NaN or zero values)
    # If you want to skip rendering specific empty regions, we'll replace them with a placeholder value, which is what pynbody is doing from what I gather.
    # For example, setting NaN values to 0 and or skipping them visually.
    # MAY BE MODIFIED FURTHER
    empty_mask = np.isnan(img_data) | (img_data == 0) # Identifies NaN and 0 pixels via a bit wise OR
    if np.any(empty_mask):

        # Option 1: Replace empty values with some default (like 0)
        img_data[empty_mask] = 0  # Pretty sure this is what pynbody does. This may break everything. Test with caution.

        # Option 2: Skip rendering those elements (no action needed, just handle it visually). Again, I don't know if this does much.

        # Update the plot with modified data
        galaxy.set_array(img_data)

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

    # Checking if the dataset is empty in of itself (e.g., no stars or gas in the region) 
    chunk_check (sim[qty])
                      
    # defining the initial z [TO BE MADE ADJUSTABLE]
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

            # Define the z-range for this specific frame
            z_min = z - z_shift / 2
            z_max = z + z_shift / 2

            # Filter the galaxy data for the current frame's z-layer
            current_frame_data = sim['pos'][(sim['pos'][:, 2] >= z_min) & (sim['pos'][:, 2] < z_max)]

            # Checking if there is data in the current frame's slice
            chunk_check (current_frame_data)

            # Plotting the Next Frame
            galaxy.remove()  # Clear the imshow artist to avoid overlapping images
            galaxy = pyn.plot.sph.image(sim, width=width, qty=qty, vmin=vmin, vmax=vmax, cmap=cmap, subplot=ax, ret_im=True)

            bit_check (galaxy)

            # Updating plotText
            z += z_shift
            ptext.set_text(f'z = {z:.3f} kpc')

            return galaxy

    # Initializing the animation
    ani = animation.FuncAnimation(fig, func=update, frames=frames, interval=interval, **kwargs)

    return ani
