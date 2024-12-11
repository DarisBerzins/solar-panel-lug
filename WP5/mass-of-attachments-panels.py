import numpy as np

#=====================================================
#INPUTS

m_NTO = 408.45 # mass of nitrogen tetroxide propellant 
m_MMO = 247.54 # mass of hydrazine propellant

m_tank = 17.5 # mass of each propellant tank

launchGForce = 12 # assumed g-force during launch

safetyFactor = 2.5 # safety factor for attachment bracket sizing

materials = [ # yield stress, density, name
    [215e6, 8000, "304 stainless steel"],
    [193e6, 2680, "aluminum 5052"],
    [450e6, 7870, "aisi 1046 steel"]
]

#====================================================
#CODE

m_NTO += m_tank
m_MMO += m_tank

f_NTO = m_NTO * launchGForce * 9.81 * safetyFactor
f_MMO = m_MMO * launchGForce * 9.81 * safetyFactor

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


lowestMassMMO = 999999999999
lowestMassNTO = 999999999999
for material in materials:
    #MMO Tank
    for attachmentCount in range(1, 100):
        if (MassFromYield(f_MMO/attachmentCount, material) * attachmentCount) < lowestMassMMO:
            lowestMassMMO = MassFromYield(f_MMO/attachmentCount, material) * attachmentCount
            numberOfFastenersMMO = attachmentCount
            lightestMaterialMMO = material
    
    #NTO Tank
    for attachmentCount in range(1, 100):
        if (MassFromYield(f_NTO/attachmentCount, material) * attachmentCount) < lowestMassNTO:
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

class transversePanelClass():
    def __init__(self):
        pass
    