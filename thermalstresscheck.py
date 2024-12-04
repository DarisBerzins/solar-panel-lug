import numpy as np

maxSolarPanelTemperature = 383.15#in Kelvins
minSolarPanelTemperature = 168.15#in Kelvins

assemblyReferenceTemperature = 288.15#in Kelvins

def FindAttachedPartCompliance(thickness, Emoda, D_f0, D_fi): #apply formula to calcuate compliance of part
    return ( 4*thickness ) / ( Emoda * np.pi * ( D_f0**2 - D_fi**2 ) )

def FindFastenerCompliance(Emodb, SubsL, SubsA):
    '''Takes a young modulus and two lists with segment lengths and segment areas, returns fastener compliance duh'''
    return (1/Emodb) * np.sum(np.divide(SubsL, SubsA))

alphaFastener = 1
alphaLug = 1
alphaSpacecraftWall = 1
fastenerCompliance = 1
attachedPartCompliance = 1
forceRatio = attachedPartCompliance/(attachedPartCompliance + fastenerCompliance)

def ForceRatio(attachedPartCompliance, fastenerCompliance):
    return attachedPartCompliance/(attachedPartCompliance + fastenerCompliance)


def FindThermalLoad(alphaFastener, alphaClampedPart, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio):#apply formula from book to calculate thermal load in fasteners
    return (alphaClampedPart - alphaFastener) * deltaT * fastenerElasticModulus * fastenerStiffnessArea * (1 - jointForceRatio)

