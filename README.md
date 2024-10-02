# Title:           Galactic Simulation Movie Creator (dancing_Galaxies) Repository
# Authors: Karl Caruana & Michael Hall      
# Last Updated:    01/10/2024

(Work in progress. To be formatted soon.)

Repository User Guide:

- Imageio vs. Matplotlib FuncAnimation (and the used packages and libraries)
  
    This repository is based on the FuncAnimation class within Matplotlib animation to create the so-called movies. An alternative method may be the Imageio python library to create GIFs. Please find a sample use thereof in this repository; https://github.com/Karl-Caruana/dancingGalaxiesButGIFs/blob/main/astro_phy_gif_creator.py.

    [Please note that this is not under development and is merely linked for those curious about alternative code methodologies. FuncAnimation was chosen as it seemed to be more versatile and generally applicable for our purposes.]

    Associated/Used library and package imports;
        - import pynbody as pyn
        - import matplotlib
        - import matplotlib.pyplot as plt
        - import matplotlib.animation as animation
        - from matplotlib.animation import FuncAnimation
        - import numpy as np
        - from tqdm import tqdm # progress bar
        - import os # operating system access
        - import gc  # garbage collection
  
- ffmeg Installation Guide
     We use ffmeg for saving the resulting animations therefor; ... https://ffmpeg.org/
  
- Structure (examples, misc mains, misc others, behemoth min, checks renderers sandbox and writers)
     Examples contains the time and z spanning examples.
     misc contains the miscellaneous python files of user inputs, stars by ages, and two main versions. The latter served as the basis for the code currently being worked on.
     behmoth minimal is the basis of what was used to create the animations sent via email
    checks, rendered, sandbox and writers are those used in conjunction (the other part of the main code)

Code User Guide

   - Explanation per segment and in whole
       in sandbox call the renderers then the writers
