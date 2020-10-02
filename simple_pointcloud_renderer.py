# -*- coding: utf-8 -*-
"""
    Simple VTK Point Cloud Rendered using PyVista Library

    Author: Jari Honkanen

"""

import numpy as np
import pyvista as pv
from pyvista import examples

def generate_points(decimateFactor = 0.05):
    """ Create numpy array of points from PyVista LiDAR example """
    
    # Get PyVista Lidar Example Data
    print("Downloading PyVista LiDAR Example data ...")
    dataset = examples.download_lidar()
    print(f"Downloading complete. Downloaded {dataset.n_points} points.")
    # Get random points from the dataset
    pointIds = np.random.randint(low=0, high=dataset.n_points-1, size=int(dataset.n_points * decimateFactor) )
    print(f"Number of points after decimation: {len(pointIds)}")

    return dataset.points[pointIds]



if __name__ == "__main__":

    # Get points
    pointArray = generate_points()

    # Create a PyVista Mesh
    pointCloud = pv.PolyData(pointArray)

    # Plot PyVista mesh
    pointCloud.plot(eye_dome_lighting=True)  

