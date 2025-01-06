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
        self.attachmentCounts = [] #these connect to the central cylindrical shell
        self.forcesPerAttachment = []
        self.closingPanelAttachmentCounts = [] #these connect the closing panels to the transverse panels
        self.attachmentMass = 0
        self.fastenerMass = 0

    def initPanel(self, componentMasses, attachmentCount): #mass of components plus transverse sandwich panel
        totalToAdd = sum(componentMasses) + findSandwichMass((self.sideLength * self.sideWidth) - (np.pi * (self.cylinderDiameter / 2) ** 2))
        self.panelMasses.append(totalToAdd)
        self.attachmentCounts.append(attachmentCount)
        self.closingPanelAttachmentCounts.append(0)
        self.forcesPerAttachment.append(0)
        
    def addClosingPanels(self):
        areaWidthPanel = self.sideWidth * self.sideHeight
        areaLengthPanel = self.sideLength * self.sideHeight
        massWidthPanel = findSandwichMass(areaWidthPanel)
        massLengthPanel = findSandwichMass(areaLengthPanel)
        panelCount = len(self.panelMasses) + 1
        for i in range(len(self.panelMasses)):
            self.panelMasses[i] += (2 * (massWidthPanel + massLengthPanel))/panelCount
            if len(self.closingPanelAttachmentCounts) <= i:  # it was giving an error so fixed it like this
                self.closingPanelAttachmentCounts.append(0)
            self.closingPanelAttachmentCounts[i] = 8 #assumes two attachments for each transverse panel

    def findForcesPerAttachment(self, panelNr):
        while len(self.forcesPerAttachment) <= panelNr:  # same as with closing panels, got an error
            self.forcesPerAttachment.append(0)
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


panel_properties = {
    'acceleration': launchGForce * 9.81,
    'sideLength': 1.400,
    'sideHeight': 0.0153961,
    'sideWidth': 0.830,
    'cylinderDiameter': 0.805,
    'fastenersPerAttachment': 4
}

all_components = [  # STILL ADD SOME MASSES
    [
        {'name': 'nothing', 'mass': 0.0},
    ],
    [
        {'name': 'Power Distribution Unit', 'mass': 1},
        {'name': 'Battery', 'mass': 5.9},
        {'name': 'IMU', 'mass': 6.85},
        {'name': 'HRSC camera', 'mass': 11.8},
        {'name': 'HRSC electronics', 'mass': 7.2},
        {'name': 'Star Sensor', 'mass': 0.470},
    ],
    [
        {'name': 'RLG module', 'mass': 1.816},
        {'name': 'Wheel Drive Electronics', 'mass': 4.67},
        {'name': 'Reaction Wheels', 'mass': 24.08},
        {'name': 'Altimeter', 'mass': 13},
        {'name': 'UV Spectrometer', 'mass': 14.5},
        {'name': 'UVS Electronics', 'mass': 7},
        {'name': 'Star Sensor', 'mass': 0.470},
    ],
    [
        {'name': 'Magnetometer Boom', 'mass': 30},
        {'name': 'Magelectronics', 'mass': 12},
        {'name': 'Helium Tank', 'mass': 233.54},
        {'name': 'Star Sensor', 'mass': 0.470},
        {'name': '4 Thrusters', 'mass': 1.4},
        {'name': 'Solar Panels', 'mass': 18.06},
    ],
]

panels = []
for i, components in enumerate(all_components):
    panel = transversePanelsClass(
        acceleration=panel_properties['acceleration'],
        sideLength=panel_properties['sideLength'],
        sideHeight=panel_properties['sideHeight'],
        sideWidth=panel_properties['sideWidth'],
        cylinderDiameter=panel_properties['cylinderDiameter'],
        fastenersPerAttachment=panel_properties['fastenersPerAttachment']
    )
    panels.append(panel)

    panel.initPanel([comp['mass'] for comp in components], attachmentCount=10)

    panel.addClosingPanels()
    panel.findForcesPerAttachment(panelNr=0)
    panel.designAttachments()

    print(f"Panel {i + 1}:")
    if not panel.checkBearingOK():
        print("Bearing stress exceeds limit")
    else:
        print("Bearing stress is within limit")

    if not panel.checkPullThroughOK():
        print("Pull-through stress exceeds limit")
    else:
        print("Pull-through stress is within limit")


# first three panels work with 4 attachments, fourth panel fails the bearing stress
