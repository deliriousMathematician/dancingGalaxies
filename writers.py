import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# ----------------------------------------------------------------------------------------------------------------------
# user data [REMOVE]
ffmpeg_path = "C:\\Users\\Michael\\Documents\\python\\ffmpeg\\bin\\ffmpeg.exe"
write_path = "animations/mBranch.mp4"
# ----------------------------------------------------------------------------------------------------------------------

# **kwargs for ani.save


def save_ffmpeg(ani, ffmpeg_path, write_path, fps=5, bitrate=-1, dpi=200, **kwargs):
    """

    Save animation using FFmpeg.

    **Keyword arguments:**

    *ani* : The animation object to be written to disk.

    *ffmpeg_path* : The path of the ffmpeg executable.

    *write_path* : Where the processed animation will be saved to.

    *fps* (5):  Playback speed [Frames per second] of the animation.

    * bitrate* (-1): The bitrate of the saved animation.
    Setting to -1 auto-determines optimal bitrate.

    *dpi* (200): Dots per Inch.

    **Returns:** None
    """

    # Set ffmpeg_path as source
    matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path
    writer = animation.FFMpegWriter(fps=fps, bitrate=bitrate)  # -1 for automatic best bitrate

    # Writing to path
    ani.save(write_path, writer=writer, dpi=dpi, **kwargs)

    # Cleanup to free memory
    plt.close()