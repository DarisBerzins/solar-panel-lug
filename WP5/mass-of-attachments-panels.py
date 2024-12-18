import numpy as np

#=====================================================
#INPUTS

m_NTO = 408.45 # mass of nitrogen tetroxide propellant 
m_MMO = 247.54 # mass of hydrazine propellant

m_tank = 17.5 # mass of each propellant tank

launchGForce = 12 # assumed g-force during launch

safetyFactor = 2.5 # safety factor for attachment bracket sizing

materials = [ # yield stress, density, name, bearing strength, shear yield strength
    [215e6, 8000, "304 stainless steel", 215e6, 386e6],
    [193e6, 2680, "aluminum 5052", 131e6, 124e6],
    [450e6, 7870, "aisi 1046 steel", 450e6, 430e6]
]

holeDiameter = 0.005
headDiameter = 0.008
boltDiameter = 0.0045

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

def getAttachmentProperty(ForcePerFastener, material, property):
    area = ForcePerFastener/material[0]
    if area < 0.00008: area = 0.00008
    thickness = np.sqrt(area/20)
    length = 20 * np.sqrt(area/20)
    width = length/2
    volume = 2 * (thickness * length * width) - (thickness * thickness * length)
    mass = volume * material[1]
    match property:
        case "strength": return ForcePerFastener
        case "area": return area
        case "thickness": return thickness
        case "length": return length
        case "width": return width
        case "volume": return volume
        case "mass": return mass
        case "material": return material

nomex_rho = 48.2  # kg/m^3
weavefabric_rho = 1611  # kg/m^3
fabric_t = 0.00019805  # m
nomex_t = 0.015  # m

def findSandwichMass(area):
    return  2 * (fabric_t * area) * weavefabric_rho + (nomex_t * area) * nomex_rho


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

class transversePanelsClass():
    def __init__(self, acceleration, sideLength, sideHeight, sideWidth, cylinderDiameter, fastenersPerAttachment):
        self.acceleration = acceleration
        self.sideLength = sideLength
        self.sideHeight = sideHeight
        self.sideWidth = sideWidth
        self.cylinderDiameter = cylinderDiameter
        self.fastenersPerAttachment = fastenersPerAttachment
        self.panelMasses = []
        self.attachmentCounts = []#these connect to the central cylindrical shell
        self.forcesPerAttachment = []
        self.closingPanelAttachmentCounts = [] #these connect the closing panels to the transverse panels
        self.attachmentMass = 0
        self.fastenerMass = 0

    def initPanel(self, componentMasses, attachmentCount): #mass of components plus transverse sandwich panel
        totalToAdd = sum(componentMasses) + findSandwichMass((self.sideLength * self.sideWidth) - (np.pi * (self.cylinderDiameter / 2) ** 2))
        self.panelMasses.append(totalToAdd)
        self.attachmentCounts.append(attachmentCount)
        
    def addClosingPanels(self):
        areaWidthPanel = self.sideWidth * self.sideHeight
        areaLengthPanel = self.sideLength * self.sideHeight
        massWidthPanel = findSandwichMass(areaWidthPanel)
        massLengthPanel = findSandwichMass(areaLengthPanel)
        panelCount = len(self.panelMasses) + 1
        for i in range(len(self.panelMasses)):
            self.panelMasses[i] += (2 * (massWidthPanel + massLengthPanel))/panelCount
            self.closingPanelAttachmentCounts[i] = 8 #assumes two attachments for each transverse panel

    def findForcesPerAttachment(self, panelNr):
        totalAttachments = self.attachmentCounts[panelNr] + self.closingPanelAttachmentCounts[panelNr]
        totalMass = self.panelMasses[panelNr] + totalAttachments * self.attachmentMass + totalAttachments * self.fastenersPerAttachment * self.fastenerMass
        self.forcesPerAttachment[panelNr] = (totalMass * self.acceleration)/self.attachmentCounts[panelNr]

    def designAttachments(self):
        peakForce = max(self.forcesPerAttachment)
        self.attachmentMass = getAttachmentProperty(peakForce, lightestMaterialMMO, "mass")
        self.attachmentScaleFactor = getAttachmentProperty(peakForce, lightestMaterialMMO, "thickness")/0.001

    def checkBearingOK(self): #returns false if the part fails
        MaxFastenerInPlaneLoad = max(self.forcesPerAttachment)
        FastenerCriticalBearingStress = lightestMaterialMMO[3]
        bearingStress = MaxFastenerInPlaneLoad/(holeDiameter * self.attachmentScaleFactor * 0.001)
        return bearingStress < FastenerCriticalBearingStress

    def checkPullThroughOK(self):#returns false if the part fails
        MaxFastenerOutOfPlaneLoad = max(self.forcesPerAttachment)
        FastenerCriticalPullThroughStress = lightestMaterialMMO[4]
        pullThroughArea = (np.pi / 4) * (headDiameter**2 - boltDiameter**2)
        pullThroughStress = MaxFastenerOutOfPlaneLoad / pullThroughArea
        return pullThroughStress < FastenerCriticalPullThroughStress
    
    def findForcesOnShell(self):
        pass

#init class
#add all the panels with their components
#add closing panels

#iterate lol