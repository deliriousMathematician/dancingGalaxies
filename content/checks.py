# These are some data check functions for the supplied galactic simulations. Generally reformats and encapsulates what pynbody should do with nullities.

import numpy as np
import matplotlib.pyplot as plt

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
