
# -*- coding: utf-8 -*-
"""
    Simplest possible PyVista Background plotter code

    Author: Jari Honkanen

"""

import pyvista as pv
from pyvistaqt import BackgroundPlotter

# Get Sphere shape
sphere = pv.Sphere()

# Instantiate Background Plotter
plotter = BackgroundPlotter()
plotter.add_mesh(sphere)

# Run in Python (iPython not needed)
plotter.app.exec_()

