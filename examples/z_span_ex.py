import pynbody as pyn
from content.renderers import z_span
from content.writers import save_ffmpeg

# Loading Simulation
simu = "../simFiles/run708main.01000"
h = pyn.load(simu)

# Converting units and aligning face-on
h.physical_units()
h.s['age'].convert_units('Gyr')
pyn.analysis.angmom.faceon(h)

# Example 1
ani = z_span(h.g, qty="rho", z_shift=0.001, z_max=0.25, title="Rho at various z")

# Example 2
# ani = z_span(h.s, qty="age", z_shift=0.001, z_max=0.1, vmin=0.1, vmax=10, qtytitle="age (Gyr)",
#              title='Star Age at various z', ptext_pos=(0.05, 0.05))

# Specifying Required Paths
ffmpeg_path = "C:\\Users\\...\\ffmpeg\\bin\\ffmpeg.exe"
write_path = "..\\animations\\example.mp4"

# Saving with ffmpeg
save_ffmpeg(ani, ffmpeg_path, write_path, fps=25)
