import numpy

maxSolarPanelTemperature = 383.15#in Kelvins
minSolarPanelTemperature = 168.15#in Kelvins

assemblyReferenceTemperature = 288.15#in Kelvins

alphaFastener = 1
alphaLug = 1
alphaSpacecraftWall = 1
fastenerCompliance = 1
attachedPartCompliance = 1
forceRatio = attachedPartCompliance/(attachedPartCompliance + fastenerCompliance)



def FindThermalLoad(alphaFastener, alphaClampedPart, deltaT, fastenerElasticModulus, fastenerStiffnessArea, jointForceRatio):
    return (alphaClampedPart - alphaFastener) * deltaT * fastenerElasticModulus * fastenerStiffnessArea * (1 - jointForceRatio)

