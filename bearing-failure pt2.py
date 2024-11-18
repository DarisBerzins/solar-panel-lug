import numpy as np

F = np.array([2, 1, 1])#x, y, z
CGlocation = np.array([1, 0, 1])
ForceLocation = np.array([0, 0, 0])

Fx = F[0]
Fz = F[2]

def FindMomentArm(location1, location2):
    return np.linalg.norm(location2 - location1)

distance = FindMomentArm(CGlocation, ForceLocation)


