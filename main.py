import math
import numpy as np

import assumptions
import bearingfailure as bf
import thermalstresscheck as ts

import fasterners_design as fd
import pullthroughfailure as pf
import minimumplatethicknesspullthrough as mptpf

#Constants defined here
deltaT = max(ts.maxSolarPanelTemperature - ts.assemblyReferenceTemperature, ts.assemblyReferenceTemperature - ts.minSolarPanelTemperature)


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



#calculate forces
from Loadcasecalculation import F_thruster, M_thruster
from Loadcasecalculationslew import F_launch, M_launch

#run lug design
import lug_design as ld
best_dev = ld.best_deviation
print(best_dev)#[deviation, w, t1, D1, material["number"]]

#run fastener design
fastenersDesigned = fd.optimum_configuration(best_dev[1], D2,2)
#get coordinates of all the fasteners

fasteners_amount, fasteners_v_spacing = fd.optimum_configuration(best_dev[1], D2,2)
fasteners_h_spacing = assumptions.fastener_horizontal_spacing
coordinates = []

if (fasteners_amount % 2 == 0):
    for i in fasteners_amount/2:
        y1 = (fasteners_v_spacing/2) + fasteners_v_spacing * i
        y2 = 0-y1
        x1 = fasteners_h_spacing
        x2 = 0-x1
        coordinates.append([x1, y1])
        coordinates.append([x2, y2])
else:
    coordinates.append([-fasteners_h_spacing, 0])
    coordinates.append([fasteners_h_spacing, 0])
    if fasteners_amount-1 > 0:
        for i in fasteners_amount:
            y1 = fasteners_v_spacing * i
            y2 = 0-y1
            x1 = fasteners_h_spacing
            x2 = 0-x1
            coordinates.append([x1, y1])
            coordinates.append([x2, y2])

#Fastener configuration: (Coords array, diameters array
fasteners = bf.FastenersClass(np.array(([1, 1, 1], [0, 0, 0])), np.array([2, 3]))
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


d_fi = fasteners.diameter[0]
pullThroughThicknesses = mptpf.findMinimumThickness(np.linalg.norm(ld.Fy), d_fi)
Plate1Thickness = max(Plate1Thickness, pullThroughThicknesses[0])
Plate2Thickness = max(Plate2Thickness,  pullThroughThicknesses[1])
print(Plate1Thickness)
print(Plate2Thickness)



#thermal stress check

alphaFastener = 12e-6
fastenerElasticModulus = 200e9
plate1ElasticModulus = 73.1e9
fastenerStiffnessArea = math.pi*(d_fi/2)**2


plateCompliance = ts.FindAttachedPartCompliance(Plate1Thickness, plate1ElasticModulus, )
jointForceRatio = ts.ForceRatio()

alphaPlate1 = 24.7e-6
alphaPlate2 = alphaPlate1

print(TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness,  Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio))



margin = 0
while margin > 1 and margin < 2:
    margin = TestForBearing(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength)
    print("Bearing Check: ", margin)

print("Bearing Check Incl Thermal Stress: ", TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio))
