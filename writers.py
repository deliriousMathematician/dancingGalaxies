import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def save_ffmpeg(ani, ffmpeg_path, write_path, fps=5, bitrate=-1, dpi=200, **kwargs):
    """

    Save animation using FFmpeg.

    **Keyword arguments:**

    *ani* : Animation Object
        The animation object to be written to disk.

    *ffmpeg_path* : string
        The path of the ffmpeg executable.

    *write_path* : string
        Where the processed animation will be saved to.

    *fps* : int (default: 5)
        Playback speed [Frames per second] of the animation.

    * bitrate* : int (default: -1)
        The bitrate of the saved animation. Setting to -1 auto-determines optimal bitrate.

    *dpi* : int (default: 200)
        Dots per Inch.

    **Returns:** None
    """

    # Set ffmpeg_path as source
    matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path
    writer = animation.FFMpegWriter(fps=fps, bitrate=bitrate)

    # Writing to path
    ani.save(write_path, writer=writer, dpi=dpi, **kwargs)

    # Cleanup to free memory
    plt.close()
