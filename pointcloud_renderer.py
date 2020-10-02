# -*- coding: utf-8 -*-
"""
    VTK Point Cloud Rendered using PyVista Library.
    Shows a color legend for Z dimension

    Author: Jari Honkanen

"""

import numpy as np
import math
import pyvista as pv
from pyvista import examples

def get_example_point_cloud(decimateFactor = 0.05):
    """ Create numpy array of points from PyVista LiDAR example """
    
    # Get PyVista Lidar Example Data
    print("Downloading PyVista LiDAR Example data ...")
    dataset = examples.download_lidar()
    print(f"Downloading complete. Downloaded {dataset.n_points} points")
    print(f"Data type {type(dataset)}")
    # Get random points from the dataset
    pointIds = np.random.randint(low=0, high=dataset.n_points-1, size=int(dataset.n_points * decimateFactor) )
    print(f"Number of points after decimation: {len(pointIds)}")

    return dataset.points[pointIds]


def create_ellipse_point_cloud():
    """ Create an ellipse shape point cloud for testing
    """
    points_array = []

    for Z in np.arange(-1.0, 1.0, 0.05):

        for angle in np.arange(0.0, 2*math.pi, 0.05):
    
            x = 0.5 * math.cos(angle)
            y = math.sin(angle)
            z = Z
            point = [x, y, z]

            points_array.append(point)

    return np.array(points_array)


if __name__ == "__main__":

    # Get points
    #point_array = get_example_point_cloud()
    points_array = create_ellipse_point_cloud()

    # Create a PyVista Mesh
    point_cloud = pv.PolyData(points_array)

    # Get a Z component of the point array
    zData = points_array[:,-1]

    # Add to mesh
    point_cloud["height"] = zData

    # Plot PyVista mesh
    point_cloud.plot(render_points_as_spheres=True)  

