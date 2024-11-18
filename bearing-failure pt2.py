import numpy as np

class FastenersClass():
    def __init__(self, coords, force, diameter):
        self.coords = coords
        self.force = force
        self.diameter = diameter


fasteners = FastenersClass(np.array([1, 1, 1], [0, 0, 0]), np.array([0, 0, 0],[1, 0, 0]), np.array([2, 3]))


print(fasteners.coords)

F = np.array([1, 0, 0])#x, y, z as shown in figure 4.2 of the reader
CGlocation = np.array([1, 0, 0])
ForceLocation = np.array([0, 0, 1])

Fx = F[0]
Fz = F[2]

def FindMomentArmVector(location1, vectorAtLocation1, location2):
    vectorY = location2 - location1
    projection = (np.dot(vectorY, vectorAtLocation1)/np.dot(vectorAtLocation1, vectorAtLocation1)) * vectorAtLocation1
    return projection - vectorY

# def FindInPlaneForcesOnFasteners(FastenerArray, AppliedForce, ForceLocation):
#     fastenerCG = np.array([0, 0, 0])#find cg
#     fastenerAmount = len(FastenerArray)
#     FastenerArray[:, 4] = AppliedForce[0]/fastenerAmount #FastenerArray: x, y, z, diameter, Fx, Fy, Fz
#     FastenerArray[:, 6] = AppliedForce[3]/fastenerAmount
#     momentArm = FindMomentArmVector(ForceLocation, AppliedForce, fastenerCG)
#     My = np.cross(AppliedForce, momentArm)
#     FastenerArray[:, 5] = (My * np.pi * )
