import numpy as np

class FastenersClass():
    def __init__(self, coords, force, diameter):
        '''Creates element containing parameters for all fasteners.'''
        self.coords = coords #numpy vector - [x, y, z]
        self.force = force #numpy vector = [x, y, z]
        self.diameter = diameter #float value in meters
        self.amount = len(self.coords) #find amount of fasteners
        self.cgCoords = np.array([0, 0, 0])#this is found in the other code


fasteners = FastenersClass(np.array([[1, 1, 1], [0, 0, 0]], dtype=float), np.array([[0, 0, 0],[0, 0, 0]], dtype=float), np.array([2, 3], dtype=float))


def FindMomentArmVector(location1, vectorAtLocation1, location2):
    '''Finds moment arm vector from location2 to vector passing through location1'''
    vectorY = location2 - location1#vector y in orthogonal projection
    projection = (np.dot(vectorY, vectorAtLocation1)/np.dot(vectorAtLocation1, vectorAtLocation1)) * vectorAtLocation1#orthogonal projection
    return projection - vectorY#return difference between orthogonal projection and vector y

def FindInPlaneForcesOnFasteners(fasteners, AppliedForce, ForceLocation, AppliedMomentVector):
    '''Finds in-plane forces for a provided set of fastener locations based on an applied force at a location'''
    print(fasteners.amount)
    print(AppliedForce[0])
    print(np.full((fasteners.amount), np.divide(AppliedForce[0], fasteners.amount)))
    fasteners.force = np.zeros((fasteners.amount, 3))
    fasteners.force[:, 0] += np.full((fasteners.amount), np.divide(AppliedForce[0], fasteners.amount))
    fasteners.force[:, 2] += np.full((fasteners.amount), np.divide(AppliedForce[2], fasteners.amount))
    momentArm = FindMomentArmVector(ForceLocation, AppliedForce, fasteners.cgCoords)
    My = np.cross(AppliedForce, momentArm) + AppliedMomentVector[2] # Calculate moment in the y direction using the contribution from the force vector and the y component of M
    total = 0
    for i in range(fasteners.amount):
        total += np.pi * np.square(fasteners.diameter[i]/2) * np.square(np.linalg.norm(fasteners.coords[i] - fasteners.cgCoords))
    for i in range(fasteners.amount):
        fasteners.force[i, 1] = np.divide(np.linalg.norm(My) * np.pi * np.square(fasteners.diameter[i]/2) * np.linalg.norm(fasteners.coords[i] - fasteners.cgCoords), total)

FindInPlaneForcesOnFasteners(fasteners, np.array([1, 0, 0]), np.array([1, 0, 1]), np.array([0, 1, 0]))
print(fasteners.force)