# To Do:
#   - Rendering with time and other quantities
#   - Adjust starting zPos
#   - Allow the position of the pText to be changed
#   - Allow custom Fig size to be chosen
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
pyn.analysis.angmom.faceon(h)

h.s['age'].convert_units('Gyr')

ani = z_span(h.s, qty="age", vmin=0.1, vmax=10, qtytitle="age (Gyr)", title='Star Age at various z')

ffmpeg_path = "C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
write_path = "animations/star_age.mp4"

save_ffmpeg(ani, ffmpeg_path, write_path)
