# -*- coding: utf-8 -*-
"""
    Simple VTK Point Cloud Rendered using PyVista Library.
    Shows a color legend for Z dimension

    Author: Jari Honkanen

"""

import numpy as np
import pyvista as pv
from pyvista import examples

def get_example_point_cloud(decimateFactor = 0.05):
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
    points_array = get_example_point_cloud()

    # Create a PyVista Mesh
    point_cloud = pv.PolyData(points_array)

    # Get a Z component of the point array
    zData = points_array[:,-1]

    # Add to mesh
    point_cloud["height"] = zData

    # Plot PyVista mesh
    point_cloud.plot(render_points_as_spheres=True)  

