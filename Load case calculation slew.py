import numpy as np
TorqueSC= 75 #[Nm]
Isa=1 #moment of inertia of solar array
Isc=2 #moment of inertia of spacecraft
L_cm = 0.9573 #[m]
#torque on the solar array
TorqueSA=TorqueSC*(Isa)/(Isc)
#decomposate force in function of direction of max torque and adjust for opposite direction due to being reactions
Tx=TorqueSA*np.cos(np.deg2rad(10))*np.cos(np.deg2rad(63))
Ty=TorqueSA*np.cos(np.deg2rad(10))*np.cos(np.deg2rad(27))
Tz=TorqueSA*np.cos(np.deg2rad(80)) #acting upwards
#find corresponding Force
R_y=Tz/L_cm
R_z=-Ty/L_cm
#Moments
M_x=Tx
F_launch = np.array([0, R_y, R_z])
M_launch = np.array([M_x,0,0])
print(F_launch)
print(M_launch )