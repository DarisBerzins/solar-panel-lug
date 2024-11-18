import numpy as np

F = np.array([1, 0, 0])#x, y, z
CGlocation = np.array([1, 0, 0])
ForceLocation = np.array([0, 0, 1])

Fx = F[0]
Fz = F[2]

def FindMomentArmVector(location1, vectorAtLocation1, location2):
    vectorY = location2 - location1
    projection = (np.dot(vectorY, vectorAtLocation1)/np.dot(vectorAtLocation1, vectorAtLocation1)) * vectorAtLocation1
    return projection - vectorY

def FindInPlaneForcesOnFasteners(FastenerArray, AppliedForce, ForceLocation):
    pass