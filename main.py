import numpy as np
import bearingfailure as bf
import thermalstresscheck as ts

#Constants defined here
deltaT = max(ts.maxSolarPanelTemperature - ts.assemblyReferenceTemperature, ts.assemblyReferenceTemperature - ts.minSolarPanelTemperature)

#Fastener configuration: (Coords array, diameters array
fasteners = bf.FastenersClass(np.array(([1, 1, 1], [0, 0, 0])), np.array([2, 3]))

def TestForBearing(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength):
    # Takes a whole lot of arguments and returns True if nothing breaks and False if it is not ok
    fasteners.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
    ok = fasteners.CheckBearingOK(Plate1Thickness, Plate1BearingStrength) and fasteners.CheckBearingOK(Plate2Thickness, Plate2BearingStrength)
    return ok
#========================================================================

def TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio):
    thermalLoad1 = ts.FindThermalLoad(alphaFastener, alphaPlate1, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio)
    thermalLoad2 = ts.FindThermalLoad(alphaFastener, alphaPlate2, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio)
    fasteners.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
    ok = fasteners.CheckBearingOKThermalEdition(Plate1Thickness, Plate1BearingStrength, thermalLoad1) and fasteners.CheckBearingOKThermalEdition(Plate2Thickness, Plate2BearingStrength, thermalLoad2)
    return ok


#iteration loop
while True:
    #select and design lug
    #fastener pattern
    print("Bearing Check: ", TestForBearing(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength))
    print("Bearing Check Incl Thermal Stress: ", TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio))
    #all the other failure modes