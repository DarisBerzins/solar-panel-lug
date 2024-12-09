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
    ok = fasteners.CheckBearingOK(Plate1Thickness, Plate1BearingStrength, AppliedForce, ForceLocation, AppliedMomentVector) and fasteners.CheckBearingOK(Plate2Thickness, Plate2BearingStrength, AppliedForce, ForceLocation, AppliedMomentVector)
    return ok
#========================================================================

def TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio):
    thermalLoad1 = ts.FindThermalLoad(alphaFastener, alphaPlate1, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio)
    thermalLoad2 = ts.FindThermalLoad(alphaFastener, alphaPlate2, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio)
    fasteners.FindInPlaneForces(AppliedForce, ForceLocation, AppliedMomentVector)
    ok = fasteners.CheckBearingOKThermalEdition(Plate1Thickness, Plate1BearingStrength, thermalLoad1, AppliedForce, ForceLocation, AppliedMomentVector) and fasteners.CheckBearingOKThermalEdition(Plate2Thickness, Plate2BearingStrength, thermalLoad2, AppliedForce, ForceLocation, AppliedMomentVector)
    return ok



#calculate forces
from Loadcasecalculation import F_thruster, M_thruster
from Loadcasecalculationslew import F_launch, M_launch

#run lug design
import lug_design as ld
best_dev = ld.best_deviation
print(best_dev)#[deviation, w, t1, D1, material["number"]]


#run fastener design
D2 = 0.0012
fastenersDesigned = fd.optimum_configuration(best_dev[1], D2,2)
#get coordinates of all the fasteners

fasteners_amount, fasteners_v_spacing = fd.optimum_configuration(best_dev[1], D2,2)
fasteners_h_spacing = assumptions.fastener_horizontal_spacing
coordinates = []

if (fasteners_amount % 2 == 0):
    for i in range(0, int(fasteners_amount/2)):
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
fasteners = bf.FastenersClass(np.array(coordinates), np.full((int(fasteners_amount)), D2))

#bearing and pull through iteration to find thicknesses
AppliedForce = np.add(ld.Fx, ld.Fy, ld.Fz)
print(AppliedForce)
ForceLocation = np.array([0.0, 0.0, 0.0])
print(ForceLocation)
AppliedMomentVector = np.array([25.6, -25.9, 0.0])#based on second load case 
Plate1Thickness = 0.01 #assumed thickness of vehicle wall
Plate2Thickness = 0.01 #assumed thickness of lug
Plate1BearingStrength = 441 * 10 ** 6
Plate2BearingStrength = Plate1BearingStrength
F_yi = 7143

d_fi = fasteners.diameter[0]
alphaFastener = 12e-6
fastenerElasticModulus = 200e9
plate1ElasticModulus = 73.1e9
fastenerStiffnessArea = math.pi*(d_fi/2)**2
plateCompliance = ts.FindAttachedPartCompliance(Plate1Thickness, plate1ElasticModulus, ts.D_f0, ts.D_fi)
fastenerCompliance = ts.FindFastenerCompliance(ts.Emodb, ts.SubsL, ts.SubsA)
jointForceRatio = ts.ForceRatio(plateCompliance, fastenerCompliance)

alphaPlate1 = 24.7e-6
alphaPlate2 = alphaPlate1

flag = True
justLess = False
justMore = False
while flag:
    margin = TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness,  Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio)
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



pullThroughThicknesses = mptpf.findMinimumThickness(7143, d_fi)
print(pullThroughThicknesses)
Plate1Thickness = max(Plate1Thickness, pullThroughThicknesses[0])
Plate2Thickness = max(Plate2Thickness,  pullThroughThicknesses[1])
print("Final lug thickness: " + str(Plate1Thickness))
print("Final vehicle wall thickness: " + str(Plate2Thickness))



#thermal stress check

