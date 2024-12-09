import numpy as np

maxSolarPanelTemperature = 383.15#in Kelvins
minSolarPanelTemperature = 168.15#in Kelvins

assemblyReferenceTemperature = 288.15#in Kelvins
#fastener + plates constants
E_a = 73.4 * 10e9 #Pa
# stainless steel 355
D_f0=0.002#m
D_fi=0.0012#m
Emodb=190*10**9#Pa
SubsL=[0.0007,0.004]
SubsA=[np.pi*0.002**2,2*np.pi*0.002**2]
thickness=0.023
Emoda=73*10**9
def FindAttachedPartCompliance(thickness, Emoda, D_f0, D_fi): #apply formula to calcuate compliance of part
    return ( 4*thickness ) / ( Emoda * np.pi * ( D_f0**2 - D_fi**2 ) )

def FindFastenerCompliance(Emodb, SubsL, SubsA):
    '''Takes a young modulus and two lists with segment lengths and segment areas, returns fastener compliance duh'''
    return (1/Emodb) * np.sum(np.divide(SubsL, SubsA))

alphaFastener = 1
alphaLug = 1
alphaSpacecraftWall = 1
fastenerCompliance = FindFastenerCompliance(Emodb, SubsL, SubsA)
attachedPartCompliance =FindAttachedPartCompliance(thickness, Emoda, D_f0, D_fi)
forceRatio = attachedPartCompliance/(attachedPartCompliance + fastenerCompliance)
print(attachedPartCompliance)
print(fastenerCompliance)
print(forceRatio)

def ForceRatio(attachedPartCompliance, fastenerCompliance):
    return attachedPartCompliance/(attachedPartCompliance + fastenerCompliance)


def FindThermalLoad(alphaFastener, alphaClampedPart, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio):#apply formula from book to calculate thermal load in fasteners
    return (alphaClampedPart - alphaFastener) * deltaT * fastenerElasticModulus * fastenerStiffnessArea * (1 - jointForceRatio)

