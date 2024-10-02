from content.renderers import t_span_sph
from content.writers import save_ffmpeg

# Example 1
ani = t_span_sph(snap_dir="../4movie", snap_name="run670hTDiffMetalCoolF10HRHC", base_ext_num="01700", num_snaps=51,
                 qty="rho", width=30, title="Example Title")

# Example 2
# ani = t_span_stars(snap_dir="4movie", snap_name="run670hTDiffMetalCoolF10HRHC", base_ext_num="01700", num_snaps=51,
#                    width=30)

# Specifying ffmpeg related paths
ffmpeg_path = "C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
write_path = "../animations/tspan_sph.mp4"

# Saving animation with ffmpeg
save_ffmpeg(ani, ffmpeg_path, write_path, fps=10)
