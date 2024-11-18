#this is going to calculate whether bearing failure!!!
import numpy as np

class FastenersClass():
    def __init__(self, coords, force, diameter):
        self.coords = coords # An array with vectors of the form [X, Y, Z]
        self.force = force # An array with vectors of the form [Fx, Fy, Fz]
        self.diameter = diameter # An array with elements [D]
    def getCg(self):
        # Returns a vector array of the form [CgX, CgY, CgZ]
        WeightedCoords = self.coords * np.square(self.diameter)
        self.cg = np.divide(np.sum(WeightedCoords, axis=0), np.sum(np.square(self.diameter)))
        return self.cg
    def CheckBearingOK(self, thickness, maxBearingTension):
        # Returns True if everything is indeed ok (no bearing failure), returns false if not ok (Sad fastener noises)
        # WARNING: ASSUMES WE ARE FASTENING ALIGNED WITH THE XZ PLANE
        maxAllowableForceperD = maxBearingTension * thickness
        tensions = np.divide(np.sqrt(np.square(self.force[:, 0]) + np.square(self.force[:,2])), self.diameter)
        if np.max(tensions) > maxAllowableForceperD:
            return False
        else:
            return True

fasteners = FastenersClass(np.array(([1, 1, 1], [0, 0, 0])), np.array(([0, 0, 0],[1, 0, 0])), np.array([2, 3]))


# def FindFastenerCg (FastArray):
#     # Takes an array with vectors of the form [X position, Y position, Z position, Diameter, Fx, Fy, Fz]
#     # Returns a vector of the form [CgX, CgY, CgZ]
#
#     # Multiply the position values times their area
#     FastArray[:, 0] = FastArray[:, 0] * (np.square(FastArray[:, 3]))
#     FastArray[:, 1] = FastArray[:, 1] * (np.square(FastArray[:, 3]))
#     FastArray[:, 2] = FastArray[:, 2] * (np.square(FastArray[:, 3]))
#     FastArray[:, 3] = np.square(FastArray[:, 3])
#
#     # Calculate the total area
#     total_area = np.sum(FastArray[:, 3])
#
#     # Take the average
#     CgX = np.sum(FastArray[:, 0] / total_area)
#     CgY = np.sum(FastArray[:, 1] / total_area)
#     CgZ = np.sum(FastArray[:, 2] / total_area)
#
#     return np.array([CgX, CgY, CgZ])

# def CheckBearingOK(FastArray, Plate1Thickness, Plate2Thickness, maxBearingTension1, maxBearingTension2):
#     # Takes an array with vectors of the form [X position, Y position, Z position, Diameter, Fx, Fy, Fz], the plate thickness and the allowable bearing strengths
#     # Returns True if everything is indeed ok (no bearing failure), returns false if not ok (Sad fastener noises)
#     # WARNING: ASSUMES WE ARE FASTENING ALIGNED WITH THE XZ PLANE
#     tensions1 = np.divide(np.sqrt(np.square(FastArray[:, 4]) + np.square(FastArray[:, 6])), Plate1Thickness * FastArray[:, 3])
#     tensions2 = np.divide(np.sqrt(np.square(FastArray[:, 4]) + np.square(FastArray[:, 6])), Plate2Thickness * FastArray[:, 3])
#
#     if np.max(tensions1) > maxBearingTension1 or np.max(tensions2) > maxBearingTension2:
#         return False
#     else:
#         return True
