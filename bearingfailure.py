#this is going to calculate whether bearing failure!!!
# 4.5 - 4.7
import numpy as np

class FastenersClass():
    def __init__(self, coords, diameter):
        self.coords = coords # An array with vectors of the form [X, Y, Z]
        self.diameter = diameter # An array with elements [D]
        self.amount = len(self.coords)
        self.force = np.zeros((self.amount, 3))
        self.cg = self.getCg()

    def getCg(self):
        # Returns a vector array of the form [CgX, CgY, CgZ]
        WeightedCoords = self.coords * np.square(self.diameter).reshape(-1, 1)
        self.cg = np.divide(np.sum(WeightedCoords, axis=0), np.sum(np.square(self.diameter)))
        return self.cg
    
    def CheckBearingOK(self, thickness, maxBearingTension, AppliedForce, ForceLocation, AppliedMomentVector):
        '''returns safety factor'''
        # WARNING: ASSUMES WE ARE FASTENING ALIGNED WITH THE XZ PLANE
        self.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
        maxAllowableForceperD = maxBearingTension * thickness
        tensions = np.divide(np.sqrt(np.square(self.force[:, 0]) + np.square(self.force[:,2])), self.diameter)
        maxAllowableForce = np.multiply(maxAllowableForceperD, self.diameter)
        return np.min(np.divide(maxAllowableForce, tensions))-1

    def CheckBearingOKThermalEdition(self, thickness, maxBearingTension, thermalForce, AppliedForce, ForceLocation, AppliedMomentVector):
        # Returns True if everything is indeed ok (no bearing failure), returns False if not ok (Sad fastener noises)
        # WARNING: ASSUMES WE ARE FASTENING ALIGNED WITH THE XZ PLANE
        self.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
        maxAllowableForceperD = maxBearingTension * thickness
        tensions = np.divide(thermalForce + np.sqrt(np.square(self.force[:, 0]) + np.square(self.force[:,2])), self.diameter)
        maxAllowableForce = np.multiply(maxAllowableForceperD, self.diameter)
        return np.min(np.divide(maxAllowableForce, tensions)) - 1

    def FindInPlaneForces(self, AppliedForce, ForceLocation, AppliedMomentVector):
        '''Finds in-plane forces for a provided set of fastener locations based on an applied force at a location'''
        self.cg = self.getCg()
        self.force = np.zeros((self.amount, 3))#set forces to zero as they are added to later
        self.force[:, 0] += np.full((self.amount), np.divide(AppliedForce[0], self.amount))#add forces in x-direction based on eqn. 4.2 from the reader
        self.force[:, 2] += np.full((self.amount), np.divide(AppliedForce[2], self.amount))#add forces in z-direction based on eqn. 4.3 from the reader
        momentArm = FindMomentArmVector(ForceLocation, AppliedForce, self.cg)#finds moment arm to balance force about cg
        My = np.cross(AppliedForce, momentArm) + AppliedMomentVector[2] # Calculate moment in the y direction using the contribution from the force vector and the y component of M
        total = 0#summation of areas times distance from cg^2
        for i in range(self.amount):#perform summation
            total += np.pi * np.square(self.diameter[i]/2) * np.square(np.linalg.norm(self.coords[i] - self.cg))
        for i in range(self.amount):#assign each fastener a different force in y-direction based on its distance from cg
            self.force[i, 1] = np.divide(np.linalg.norm(My) * np.pi * np.square(self.diameter[i]/2) * np.linalg.norm(self.coords[i] - self.cg), total)
        return self.force

def FindMomentArmVector(location1, vectorAtLocation1, location2):
    '''Finds moment arm vector from location2 to vector passing through location1'''
    vectorY = location2 - location1#vector y in orthogonal projection
    projection = (np.dot(vectorY, vectorAtLocation1)/np.dot(vectorAtLocation1, vectorAtLocation1)) * vectorAtLocation1#orthogonal projection
    return projection - vectorY#return difference between orthogonal projection and vector y

fasteners = FastenersClass(np.array(([1, 1, 1], [0, 0, 0])), np.array([2, 3]))

print(fasteners.getCg())
print(fasteners.CheckBearingOK(0.1, 0.1, np.array(([1.0,1.0,1.0])), np.array(([1.0,1.0,1.0])), np.array(([1.0,1.0,1.0]))))

#balls

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
