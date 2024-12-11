import numpy as np

#=====================================================
#INPUTS

class loadCasesClass():
    def __init__(self):
        self.forceCases = np.array([
            [-27.051075, -27.051075, -324.6129],
            [27.051075, 27.051075, -324.6129],
            [108.2043, 108.2043, -189.357525],
            [108.2043, 108.2043, 81.153225],
            [27.051075, 27.051075, 108.2043],
            [-27.051075, -27.051075, 108.2043],
            [-108.2043, -108.2043, 81.153225],
            [-108.2043, -108.2043, -189.357525],
            [511, 0., 0.],
            [0, 0.58267596, -2.76294769],
            [511, 108.2043, -324.6129]
        ])
        self.momentCases = np.array([
            [-25.8959941,  25.8959941,   0.],
            [25.8959941, -25.8959941,   0.],
            [103.58397639, -103.58397639,    0.],
            [103.58397639, -103.58397639,    0.],
            [25.8959941, -25.8959941,   0.],
            [-25.8959941,  25.8959941,   0.],
            [-103.58397639,  103.58397639,    0.],
            [-103.58397639,  103.58397639,    0.],
            [0, 0, 910.7553],
            [0.10754075, 0, 0],
            [103.58397639, -103.58397639, 910.7553]
        ])
loadCases = loadCasesClass()

loadCases.resultantForces = np.linalg.norm(loadCases.forceCases, axis=1)

largestResultantIndex = np.argmax(loadCases.resultantForces)

largestResultant = loadCases.resultantForces[largestResultantIndex]

m_NTO = 408.45 + 247.54
m_MMO = 247.54

launchGForce = 12

f_NTO = m_NTO * launchGForce * 9.81
f_MMO = m_MMO * launchGForce * 9.81

largestResultant = (m_NTO + m_MMO) * 12 * 9.81

tanks = [m_NTO, m_MMO]

LBracketYieldStrength = 215e6
LBracketDensity = 8000

materials = [
    [215e6, 8000, "304 stainless steel"],
    [193e6, 2680, "aluminum 5052"],
    [450e6, 7870, "aisi 1046 steel"]
]

#====================================================
#CODE

def MassFromYield(ForcePerFastener, material):
    area = ForcePerFastener/material[0]
    thickness = np.sqrt(area/20)
    length = 20 * np.sqrt(area/20)
    width = length/2
    volume = 2 * (thickness * length * width) - (thickness * thickness * length)
    mass = volume * material[1]
    if width < 0.02:
        mass = 9999999999999999999999
    return mass

def printAttachmentDimensions(ForcePerFastener, material):
    area = ForcePerFastener/material[0]
    thickness = np.sqrt(area/20)
    length = 20 * np.sqrt(area/20)
    width = length/2
    volume = 2 * (thickness * length * width) - (thickness * thickness * length)
    mass = volume * material[1]
    print("Strength: " + str(ForcePerFastener))
    print("Area: " + str(area))
    print("Thickness: " + str(thickness))
    print("Length: " + str(length))
    print("Width: " + str(width))
    print("Volume: " + str(volume))
    print("Mass: " + str(mass))
    print("Material: " + material[2])


lowestMass = 999999999999
for material in materials:
    #MMO Tank
    for attachmentCount in range(1, 100):
        if (MassFromYield(f_MMO/attachmentCount, material) * attachmentCount) < lowestMass:
            lowestMassMMO = MassFromYield(f_MMO/attachmentCount, material) * attachmentCount
            numberOfFastenersMMO = attachmentCount
            lightestMaterialMMO = material
    
    #NTO Tank
    for attachmentCount in range(1, 100):
        if (MassFromYield(f_NTO/attachmentCount, material) * attachmentCount) < lowestMass:
            lowestMassNTO = MassFromYield(f_NTO/attachmentCount, material) * attachmentCount
            numberOfFastenersNTO = attachmentCount
            lightestMaterialNTO = material

print("MMO Tank:")
printAttachmentDimensions(f_MMO/numberOfFastenersMMO, lightestMaterialMMO)
print(numberOfFastenersMMO)
print(lowestMassMMO)

print("NTO Tank:")
printAttachmentDimensions(f_NTO/numberOfFastenersNTO, lightestMaterialNTO)
print(numberOfFastenersNTO)
print(lowestMassNTO)