# To Do:
#   - Adjust starting zPos [see test.py]
#   - Figure out what to do with nullspace [ex: when plotting star age but no stars exist in the region]
#   - ...

# Bug Fixes:
#   - Animation now starts at 0.00 kpc
#   - FFmpeg saving animation properly, issue was with windows media player - use vlc
#   - ...

# Done:
#   - sideOn/faceOn view to be set by user before running function
#   - Much higher resolution thanks to adjustable dpi
#   - Defined both renderer and writer functions to handle animating
#   - Automatically determine vmin and vmax unless specified otherwise
#   - Allow custom Fig size to be chosen
#   - Allow the position of the pText to be changed
#   - ...

# ----------------------------------------------------------------------------------------------------------------------

# An example as to how one would use the dancingGalaxies Package

import pynbody as pyn
from renderers import z_span
from writers import save_ffmpeg

# Loading Simulation
simu = "simFiles/run708main.01000"
h = pyn.load(simu)

# Converting units and aligning face-on
h.physical_units()
h.s['age'].convert_units('Gyr')
pyn.analysis.angmom.faceon(h)

# Example 1
# ani = z_span(h.g, qty="rho", z_shift=0.001, title="Rho at various z")

# Example 2
ani = z_span(h.s, qty="age", z_shift=0.001, z_max=0.1, vmin=0.1, vmax=10, qtytitle="age (Gyr)",
             title='Star Age at various z', ptext_pos=(0.05, 0.05))

# Specifying Required Paths
ffmpeg_path = "C:\\Users\\micha\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
write_path = "animations\\Example1.mp4"

# Saving with ffmpeg
save_ffmpeg(ani, ffmpeg_path, write_path, fps=25)
