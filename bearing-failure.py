#this is going to calculate whether bearing failure!!!
import numpy as np

print("hello world")

def FindFastenerCg (FastArray):
    # Takes an array with vectors of the form [X position, Y position, Z position, Diameter, Fx, Fy, Fz]
    # Returns a vector of the form [CgX, CgY]

    # Multiply the position values times their area
    FastArray[:, 0] = FastArray[:, 0] * ((FastArray[:, 3]) ** 2)
    FastArray[:, 1] = FastArray[:, 1] * ((FastArray[:, 3]) ** 2)
    FastArray[:, 2] = FastArray[:, 2] * ((FastArray[:, 3]) ** 2)
    FastArray[:, 3] = (FastArray[:, 3] ** 2)

    # Calculate the total area
    total_area = np.sum(FastArray[:, 3])
    print(total_area)

    # Take the average
    CgX = np.sum(FastArray[:, 0] / total_area)
    CgY = np.sum(FastArray[:, 1] / total_area)
    CgZ = np.sum(FastArray[:, 2] / total_area)

    return np.array([CgX, CgY, CgZ])

def CheckBearingOK(FastArray, Plate1Thickness, Plate2Thickness, maxBearingTension1, maxBearingTension2):
    # Takes an array with vectors of the form [X position, Y position, Z position, Diameter, Fx, Fy, Fz], the plate thickness and the allowable bearing strengths
    # Returns True if everything is indeed ok (no bearing failure), returns false if not ok (Sad fastener noises)

