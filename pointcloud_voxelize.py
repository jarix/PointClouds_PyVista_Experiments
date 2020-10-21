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


def create_ellipse_points(radius=0.5, height=2.0, step=0.05, x_offset=0.0, y_offset=0.0, z_offset=0.0):
    """ Create an ellipse shape points array for testing
    """
    points_array = []

    z_range = abs(height/2)

    for z in np.arange(-z_range, z_range, step):

        for angle in np.arange(0.0, 2*math.pi, step):
    
            x = radius * math.cos(angle)
            y = math.sin(angle)
            point = [x + x_offset, y + y_offset, z + z_offset]

            points_array.append(point)

    return np.array(points_array)


def create_box_points(x_size=1.0, y_size=1.0, z_size=1.0, step=0.05, x_offset=0.0, y_offset=0.0, z_offset=0.0):
    """ Create an box shape points array for testing
    """
    points_array = []
    x_range = abs(x_size/2)
    y_range = abs(y_size/2)
    z_range = abs(x_size/2)
    
    for z in [-z_range, z_range]:
        for x in np.arange(-x_range, x_range, step):
            for y in np.arange(-y_range, y_range, step):
                point = [x + x_offset, y + y_offset, z + z_offset]
                points_array.append(point)

    for y in [-y_range, y_range]:
        for x in np.arange(-x_range, x_range, step):
            for z in np.arange(-z_range, z_range, step):
                point = [x + x_offset, y + y_offset, z + z_offset]
                points_array.append(point)

    for x in [-x_range, x_range]:
        for y in np.arange(-y_range, y_range, step):
            for z in np.arange(-z_range, z_range, step):
                point = [x + x_offset, y + y_offset, z + z_offset]
                points_array.append(point)

    return np.array(points_array)
 

if __name__ == "__main__":

    # Get points
    #point_array = get_example_point_cloud()
    points_array1 = create_ellipse_points(x_offset=1.0, y_offset=2.0, z_offset=3.0)
    print(f"Points Array1 type: {type(points_array1)}")
    print(f"Points Array1 shape: {points_array1.shape}")
    points_array2 = create_box_points(x_size=2.0, y_size=2.0, z_size=2.0, step=0.04)
    print(f"Points Array2 type: {type(points_array2)}")
    print(f"Points Array2 shape: {points_array2.shape}")

    points_array = np.concatenate((points_array1, points_array2), axis=0)
    print(f"Points Array type: {type(points_array)}")
    print(f"Points Array shape: {points_array.shape}")

    # Create PyVista Meshes
    point_cloud = pv.PolyData(points_array)

    voxels = pv.voxelize(point_cloud, density=0.05)
    p = pv.Plotter()
    p.add_mesh(voxels, color=True, show_edges=True, opacity=0.5)
    p.add_mesh(point_cloud, color="lightblue", opacity = 0.5)
    p.show()

    # Get a Z component of the point array
    #zData = points_array[:,-1]
    xData = points_array[:,0]
    print(f"xData points Array type: {type(xData)}")
    print(f"xData points Array shape: {xData.shape}")  
    # Add to mesh
    #point_cloud["height"] = zData
    point_cloud["distance"] = xData

    # Plot PyVista mesh
    point_cloud.plot(render_points_as_spheres=True)  

