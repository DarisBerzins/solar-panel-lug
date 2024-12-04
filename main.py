import numpy as np

import assumptions
import bearingfailure as bf
import thermalstresscheck as ts

import fasterners_design as fd
import pullthroughfailure as pf

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

#thermal stress check




margin = 0
while margin > 1 and margin < 2:
    margin = TestForBearing(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength)
    print("Bearing Check: ", margin)

print("Bearing Check Incl Thermal Stress: ", TestForBearingIncludingThermalStress(AppliedForce, ForceLocation, AppliedMomentVector, Plate1Thickness, Plate2Thickness, Plate1BearingStrength, Plate2BearingStrength, alphaFastener, alphaPlate1, alphaPlate2, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio))
