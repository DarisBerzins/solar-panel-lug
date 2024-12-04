import numpy as np
import bearingfailure as bf
import thermalstresscheck as ts

import fasterners_design as fd
import pullthroughfailure as pf

#Constants defined here
deltaT = max(ts.maxSolarPanelTemperature - ts.assemblyReferenceTemperature, ts.assemblyReferenceTemperature - ts.minSolarPanelTemperature)

#Fastener configuration: (Coords array, diameters array
fasteners = bf.FastenersClass(np.array(([1, 1, 1], [0, 0, 0])), np.array([2, 3]))

def TestForBearing(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength):
    # Takes a whole lot of arguments and returns True if nothing breaks and False if it is not ok
    fasteners.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
    ok = fasteners.CheckBearingOK(Plate1Thickness, Plate1BearingStrength, AppliedForce, ForceLocation, AppliedMomentVector) and fasteners.CheckBearingOK(Plate2Thickness, Plate2BearingStrength, AppliedForce, ForceLocation, AppliedMomentVector)
    return ok
#========================================================================

def TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio):
    thermalLoad1 = ts.FindThermalLoad(alphaFastener, alphaPlate1, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio)
    thermalLoad2 = ts.FindThermalLoad(alphaFastener, alphaPlate2, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio)
    fasteners.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
    ok = fasteners.CheckBearingOKThermalEdition(Plate1Thickness, Plate1BearingStrength, thermalLoad1) and fasteners.CheckBearingOKThermalEdition(Plate2Thickness, Plate2BearingStrength, thermalLoad2)
    return ok



#run lug design
import lug_design as ld
print(ld.best_deviation)#[deviation, w, t1, D1, material["number"]]

#run fastener design
# fastenersDesigned = fd.optimum_configuration(ld.best_deviation[1], 1.2, 2.0)
#get coordinates of all the fasteners

#bearing and pull through iteration to find thicknesses
AppliedForce = ld.Fx + ld.Fy + ld.Fz
ForceLocation = np.array([0.0, 0.0, 0.0])
AppliedMomentVector = np.array([25.6, -25.9, 0.0])#based on second load case 
Plate1Thickness = 0.01 #assumed thickness of vehicle wall
Plate2Thickness = 0.01 #assumed thickness of lug
Plate1BearingStrength = 441 * 10 ** 6
Plate2BearingStrength = Plate1BearingStrength
flag = True
justLess = False
justMore = False
while flag:
    margin = TestForBearing(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength)
    print("Bearing margin: ", margin)
    
    if justLess and justMore: break
    if margin < 1: 
        Plate1Thickness += 0.0001
        Plate2Thickness += 0.0001
        justLess = True
    elif margin > 1.05:
        Plate1Thickness -= 0.0001
        Plate2Thickness -= 0.0001
        justMore = True
    else:
        flag = False
    print(Plate1Thickness, Plate2Thickness)

#thermal stress check






# print("Bearing Check Incl Thermal Stress: ", TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio))
