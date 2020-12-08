# -*- coding: utf-8 -*-
"""
    Point Cloud Class
	
	Supports reading point clouds from PCD files and writing them to PCD files

	Author: Jari Honkanen

"""
import numpy as np

# point types
unsigned_types = { 1: np.uint8, 2: np.uint16, 4: np.uint32 }
signed_types = { 1: np.int8, 2: np.int16, 4: np.int32 }
float_types = { 4: np.float32, 8: np.float64 }


class PointCloud:
    """ PointCloud class supporting file I/O and format conversions """

    def __init__(self):
        # Point cloud parameters
        self.file_type = None
        self.point_cloud_type = None
        self.point_type = None
        self.points_array = []
        self.points_array_full = []
        self.width = 0
        self.height = 0
        self.viewpoint = ""
        self.num_points = 0
        self.num_fields = 0


    def read_pcd_file(self, file_name, bPrint = False):
        """
        Read and parse PCD file (both Binary and ASCII files are supported)

        Parameters:
            file_name (string): Name and Path to the PCD file to be read
            bPrint (bool) : Debug print

        Returns:
            self.points_array : Numpy Array of the point cloud data

        Exceptions:
            IOError: if input file cannot be read
            TypeError:  if datatype in PCD file is not recognized
        """
        
        try:
            f = open(file_name, "rb")

        except:
            print("[ERROR]: Could not open file '" + file_name + "'")
            raise IOError

        # Read and Parse Header
        header_complete = False

        while not header_complete:

            line = f.readline()
            line = line.decode("utf-8")    # Header fields are always in ASCII
            line = line.replace('\n', '').replace('\r', '')   # Remove CRLF

            # Skip comments
            if line.startswith("#"):
                if bPrint:
                    print(line)
                continue

            if line.upper().startswith("VERSION"):
                version = line.split(' ')[1]
                if (bPrint):
                    print("Version: " + version)
                continue

            if line.upper().startswith("FIELDS"):
                fields = line.split(' ')
                self.num_fields = len(fields) - 1
                if self.num_fields == 3:
                    self.point_cloud_type = "XYZ"
                elif self.num_fields == 4:
                    self.point_cloud_type = "XYZI"
                if (bPrint):
                    for field in fields:
                        print(field)
                continue

            if line.upper().startswith("SIZE"):
                sizes = line.split(' ')
                data_size = int(sizes[1])
                if (bPrint):
                    for size in sizes:
                        print(size)
                continue

            if line.upper().startswith("TYPE"):
                field_types = line.split(' ')
                if (bPrint):
                    for field in field_types:
                        print(field)
                field_type = field_types[1]
                continue
                
            if line.upper().startswith("COUNT"):
                counts = line.split(' ')
                if (bPrint):
                    for count in counts:
                        print(count)
                continue

            if line.upper().startswith("WIDTH"):
                self.width = int(line.split(' ')[1])
                if (bPrint):
                    print("Width: " + str(self.width))
                continue

            if line.upper().startswith("HEIGHT"):
                self.height = int(line.split(' ')[1])
                if (bPrint):
                    print("Height: " + str(self.height))
                continue

            if line.upper().startswith("VIEWPOINT"):
                self.viewpoint = line[10:]
                if (bPrint):
                    print("Viewpoint: " + self.viewpoint)
                continue

            if line.upper().startswith("POINTS"):
                points = line.split(' ')[1]
                self.num_points = int(points)
                if (bPrint): 
                    print("# of points: " + str(self.num_points))
                continue

            if line.upper().startswith("DATA"):
                self.file_type = line.upper().split(' ')[1]
                if (bPrint): 
                    print("file type: " + self.file_type)
                header_complete = True #  Exit header and start processing actual points 
                continue

        if field_type == "F":
            self.point_type = float_types[data_size]

        elif field_type == "U":
            self.point_type = unsigned_types[data_size]

        elif field_type == "I":
            self.point_type = signed_types[data_size]

        else: 
            print("[ERROR] Invalid 'TYPE' field in the PCD file: " + field_type)
            raise TypeError
            
        self.points_array = []

        # read ASCII data
        if self.file_type == "ASCII":
            self.points_array_full = np.loadtxt(f, dtype = self.point_type)

        elif self.file_type == "BINARY":
            self.points_array_full = np.fromfile(f, dtype = self.point_type)
            self.points_array_full = np.reshape(self.points_array_full, (self.num_points, self.num_fields))

        else:
            print("[ERROR] Invalid 'DATA' field in the PCD file: " + self.file_type)
            raise TypeError
                    
        f.close()

        self.points_array = self.points_array_full
        (rows, cols) = self.points_array.shape
        if cols == 4:
            # Remove intensity channel for now
            self.points_array = np.delete(self.points_array, 3, axis=1)
        
        return self.points_array


    def write_pcd_file(self, file_name, file_type = "BINARY", bPrint = False):
        """
        Write point cloud into a PCD file (both Binary and ASCII files are supported)

        Parameters:
            file_name (string) : Name and Path to the PCD file to be written
            file_type (string) : "BINARY" or "ASCII"
            bPrint (bool) : Debug Print

        Returns:

        Exceptions:
            IOError: if input file cannot be read
            ValueError: invalid input parameter 
        """        
        if file_type == "ASCII":
            flags = "w"
        elif file_type == "BINARY":
            flags = "wb"
        else:
            raise ValueError("file_type must be 'ASCII' or 'BINARY'")
        
        try:
            f = open(file_name, flags)

        except:
            print("[ERROR]: Could not open file '" + file_name + "'")
            raise IOError


        if file_type == "ASCII":
            f.write("# .PCD v.7 - Point Cloud Data file format\n")
            f.write("VERSION .7\n")
        
            if self.point_cloud_type == "XYZ":
                f.write("FIELDS x y z\n")
                f.write("SIZE 4 4 4\n")
                f.write("TYPE F F F\n")
                f.write("COUNT 1 1 1\n")
            elif self.point_cloud_type == "XYZI":
                f.write("FIELDS x y z intensity\n")
                f.write("SIZE 4 4 4 4\n")
                f.write("TYPE F F F F\n")
                f.write("COUNT 1 1 1 1\n")

            f.write("WIDTH " + str(self.width) + "\n" )
            f.write("HEIGHT " + str(self.height) + "\n")
            f.write("VIEWPOINT " + self.viewpoint + "\n")
            f.write("POINTS " + str(self.num_points) + "\n" )

            f.write("DATA ascii\n")
            for x in self.points_array_full:
                if self.point_cloud_type == "XYZ":
                    f.write(f"{x[0]:.8f} {x[1]:.8f} {x[2]:.8f}\n")
                elif self.point_cloud_type == "XYZI":
                    f.write(f"{x[0]:.8f} {x[1]:.8f} {x[2]:.8f} {x[3]:.8f}\n")

        elif file_type == "BINARY":

            f.write(b"# .PCD v.7 - Point Cloud Data file format\n")
            f.write(b"VERSION .7\n")
        
            if self.point_cloud_type == "XYZ":
                f.write(b"FIELDS x y z\n")
                f.write(b"SIZE 4 4 4\n")
                f.write(b"TYPE F F F\n")
                f.write(b"COUNT 1 1 1\n")
            elif self.point_cloud_type == "XYZI":
                f.write(b"FIELDS x y z intensity\n")
                f.write(b"SIZE 4 4 4 4\n")
                f.write(b"TYPE F F F F\n")
                f.write(b"COUNT 1 1 1 1\n")

            output_line = "WIDTH " + str(self.width) + "\n"
            f.write(output_line.encode())
            output_line = "HEIGHT " + str(self.height) + "\n"
            f.write(output_line.encode())
            output_line = "VIEWPOINT " + self.viewpoint + "\n"
            f.write(output_line.encode())
            output_line = "POINTS " + str(self.num_points) + "\n"
            f.write(output_line.encode())

            f.write(b"DATA binary\n")
            for x in self.points_array_full:
                f.write(x[0])
                f.write(x[1])
                f.write(x[2])
                if self.point_cloud_type == "XYZI":
                    f.write(x[3])

        f.close()



        
