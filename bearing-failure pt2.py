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
    fasteners.force = np.zeros((fasteners.amount, 3))#set forces to zero as they are added to later
    fasteners.force[:, 0] += np.full((fasteners.amount), np.divide(AppliedForce[0], fasteners.amount))#add forces in x-direction based on eqn. 4.2 from the reader
    fasteners.force[:, 2] += np.full((fasteners.amount), np.divide(AppliedForce[2], fasteners.amount))#add forces in z-direction based on eqn. 4.3 from the reader
    momentArm = FindMomentArmVector(ForceLocation, AppliedForce, fasteners.cgCoords)#finds moment arm to balance force about cg
    My = np.cross(AppliedForce, momentArm) + AppliedMomentVector[2] # Calculate moment in the y direction using the contribution from the force vector and the y component of M
    total = 0#summation of areas times distance from cg^2
    for i in range(fasteners.amount):#perform summation
        total += np.pi * np.square(fasteners.diameter[i]/2) * np.square(np.linalg.norm(fasteners.coords[i] - fasteners.cgCoords))
    for i in range(fasteners.amount):#assign each fastener a different force in y-direction based on its distance from cg
        fasteners.force[i, 1] = np.divide(np.linalg.norm(My) * np.pi * np.square(fasteners.diameter[i]/2) * np.linalg.norm(fasteners.coords[i] - fasteners.cgCoords), total)
