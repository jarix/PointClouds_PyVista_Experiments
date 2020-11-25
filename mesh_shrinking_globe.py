# -*- coding: utf-8 -*-
"""
    Plot a globe mesh with Background plotter and make the mesh shrink over time

    Author: Jari Honkanen

"""

import time
import numpy as np
from threading import Thread
import pyvista as pv
import pyvistaqt as pvqt
from pyvista import examples

if __name__ == "__main__":

    globe = examples.load_globe()
    globe.point_arrays['scalars'] = np.random.rand(globe.n_points)
    globe.set_active_scalars('scalars')

    # Create background plotter
    plotter_bg = pvqt.BackgroundPlotter()
    plotter_bg.add_mesh(globe, scalars='scalars', lighting=False, show_edges=True, texture=True)
    plotter_bg.view_isometric()

    # Change globe size in the background
    def change_size():
        for i in range(50):
            globe.points *= 0.95
            globe.point_arrays['scalars'] = np.random.rand(globe.n_points)
            time.sleep(0.5)

    thread = Thread(target=change_size)
    thread.start()

    plotter_bg.app.exec_()




