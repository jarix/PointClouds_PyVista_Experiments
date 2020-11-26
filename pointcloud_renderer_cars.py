# -*- coding: utf-8 -*-
"""
    VTK Point Cloud Rendered using PyVista Library
    Create and render car shapes

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


def create_ellipse_points(radius=0.5, height=2.0, step=0.05, x_pos=0.0, y_pos=0.0, z_pos=0.0):
    """ Create an ellipse shape points array
    """
    points_array = []

    z_range = abs(height/2)

    for z in np.arange(-z_range, z_range, step):

        for angle in np.arange(0.0, 2*math.pi, step):
    
            x = radius * math.cos(angle)
            y = math.sin(angle)
            point = [x + x_pos, y + y_pos, z + z_pos]

            points_array.append(point)

    return np.array(points_array)


def create_torus_points(torus_radius=1.0, tube_radius=0.4, step=0.05, x_pos=0.0, y_pos=0.0, z_pos=0.0):
    """ Create an trous shape points array
    """
    points_array = []

    for theta in np.arange(0.0, 2*math.pi, step):

        for phi in np.arange(0.0, 2*math.pi, step):
    
            x = (torus_radius + tube_radius * math.cos(theta))*math.cos(phi)
            z = (torus_radius + tube_radius * math.cos(theta))*math.sin(phi)
            y = tube_radius*math.sin(theta)
            point = [x + x_pos, y + y_pos, z + z_pos]

            points_array.append(point)

    return np.array(points_array)



def create_box_points(x_size=1.0, y_size=1.0, z_size=1.0, step=0.05, x_pos=0.0, y_pos=0.0, z_pos=0.0):
    """ Create an box shape points array 
    """
    points_array = []

    for z in [0, z_size]:
        for x in np.arange(0.0, x_size, step):
            for y in np.arange(0.0, y_size, step):
                point = [x + x_pos, y + y_pos, z + z_pos]
                points_array.append(point)

    for y in [0, y_size]:
        for x in np.arange(0, x_size, step):
            for z in np.arange(0, z_size, step):
                point = [x + x_pos, y + y_pos, z + z_pos]
                points_array.append(point)

    for x in [0, x_size]:
        for y in np.arange(0.0, y_size, step):
            for z in np.arange(0.0, z_size, step):
                point = [x + x_pos, y + y_pos, z + z_pos]
                points_array.append(point)

    return np.array(points_array)
 

def create_car_sedan_points(x_size=4.1, y_size=1.8, z_size=1.5, step=0.05, x_pos=0.0, y_pos=0.0, z_pos=0.0):
    # Typical Sedan
    # Length = 4.1m, Width = 1.8m, height = 1.5m

    body_lower = create_box_points(x_size, y_size, 0.5*z_size, step, x_pos, y_pos, z_pos)
    body_upper = create_box_points(0.5*x_size, 0.9*y_size, 0.5*z_size, step, x_pos + 0.25*x_size, y_pos + 0.05*y_size, z_pos + 0.5*z_size)
    wheel_rr = create_torus_points(torus_radius=0.15*z_size, tube_radius=0.05*z_size, step=2*step,
        x_pos=x_pos + 0.2*x_size, y_pos=y_pos, z_pos=z_pos)
    wheel_rf = create_torus_points(torus_radius=0.15*z_size, tube_radius=0.05*z_size, step=2*step,
        x_pos=x_pos + 0.8*x_size, y_pos=y_pos, z_pos=z_pos)  
    wheel_lr = create_torus_points(torus_radius=0.15*z_size, tube_radius=0.05*z_size, step=2*step,
        x_pos=x_pos + 0.2*x_size, y_pos=y_pos + y_size, z_pos=z_pos)
    wheel_lf = create_torus_points(torus_radius=0.15*z_size, tube_radius=0.05*z_size, step=2*step,
        x_pos=x_pos + 0.8*x_size, y_pos=y_pos + y_size, z_pos=z_pos)            

    car = np.concatenate((body_lower, body_upper, wheel_rr, wheel_rf, wheel_lr, wheel_lf), axis=0)

    #return upper_body
    return car



class Car:
    """ Simple Car Point Cloud Class """
    def __init__(self, x_size=4.1, y_size=1.8, z_size=1.5, step=0.05):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.step = step

    def setSize(self, x_size=4.1, y_size=1.8, z_size=1.5, step=0.05):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.step = step

    def spawn(self, x_pos = 0.0, y_pos=0.0, z_pos=0.0):
        return create_car_sedan_points(self.x_size, self.y_size, self.z_size, self.step, x_pos, y_pos, z_pos)



if __name__ == "__main__":

    car1 = Car()
    car1_points = car1.spawn()
    car2 = Car()
    car2_points = car2.spawn(x_pos = 5.0, y_pos = 2.5)
    points_array = np.concatenate((car1_points, car2_points), axis=0)

    # Create PyVista Mesh
    point_cloud = pv.PolyData(points_array)

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

    
    

