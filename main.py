import numpy as np
import bearingfailure as bf

#Fastener configuration: (Coords array, diameters array
fasteners = bf.FastenersClass(np.array(([1, 1, 1], [0, 0, 0])), np.array([2, 3]))

def TestForBearing(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength):
    # Takes a whole lot of arguments and returns True if nothing breaks and False if it is not ok
    fasteners.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
    ok = fasteners.CheckBearingOK(Plate1Thickness, Plate1BearingStrength) and fasteners.CheckBearingOK(Plate2Thickness, Plate2BearingStrength)
    return ok
#========================================================================


