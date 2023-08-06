"""
3D coupled grid generator

Grid generator, used primarily for 'painting' shapes in 3D on multiple grids which represent the
 same spatial region, but are offset from each other. It does straightforward natural <-> grid unit
 conversion and can handle non-uniform rectangular grids (the entire grid is generated based on
 the coordinates of the boundary points along each axis).

Its primary purpose is for drawing Yee grids for electromagnetic simulations.


Dependencies:
- numpy
- matplotlib            [Grid.visualize_*]
- mpl_toolkits.mplot3d  [Grid.visualize_isosurface()]
- skimage               [Grid.visualize_isosurface()]
"""

import pathlib

from .error import GridError
from .direction import Direction
from .grid import Grid

__author__ = 'Jan Petykiewicz'

with open(pathlib.Path(__file__).parent / 'VERSION', 'r') as f:
    __version__ = f.read().strip()
version = __version__
