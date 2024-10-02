# dancing_galaxies Repository
## Galactic Simulation Movie Creator
##### Authors: Karl Caruana & Michael Hall
##### Last Updated: 02/10/2024

This project is based on the pynbody python package and animations are rendered by stitching snapshots together using ``matplotlib.animation.FuncAnimation``.

### **User Guide:**

#### 1. Installing ffmpeg:
Currently, the only writer implemented is ffmpeg. It can be installed from [here](https://www.ffmpeg.org).

#### 2. Package Imports:
Ensure your python interpreter has these packages installed:
* [pynbody](https://github.com/pynbody/pynbody)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [numpy](https://github.com/numpy/numpy)

While not being necessary, some files in ``misc`` also require:
* [tqdm](https://github.com/tqdm/tqdm)

#### 3. Importing dancing_galaxies Functions:
It is recommended that you download the ``content`` directory - within which all relevant functions related to the rendering and writing of galactic animations are located. Functions of particular interest can be found in:
* ``renderers.py``
* ``writers.py``
  
It is important that both these files be imported into your code. The former, as the name implies, deals with the rendering of animations, whereas the latter writes said renders to disk. A detailed description of each function's arguments and properties can be found commented within their respective files. 

#### 4. Using dancing_galaxies:
Each function in renderers.py works slightly differently; as such, it is highly recommended that you view the ``examples`` directory, and use the relevant example file as a template for your use-case. Behemoth minimal may serve as a good introduction to understanding the basic logic thereof. (Note that that file does have some untested experimental functions that are not required.)

---

As already mentioned, this repository is based on ``matplotlib.animation.FuncAnimation``. An alternative to this may be the [imageio](https://github.com/imageio/imageio) library. A sample use thereof can be found [here](https://github.com/Karl-Caruana/dancingGalaxiesButGIFs/blob/main/astro_phy_gif_creator.py). **(Please note that this is not under development and is merely linked for those curious about alternative code methodologies. FuncAnimation was chosen as it seemed to be more versatile and generally applicable for our purposes.)**
