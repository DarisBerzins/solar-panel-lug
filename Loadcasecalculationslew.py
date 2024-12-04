import numpy as np
from Momentofinertiaofsolararray import I_total_xx,I_total_yy,I_total_zz
TorqueSC= 75 #[Nm]
Isa=[I_total_xx,I_total_yy,I_total_zz]#moment of inertia of solar array
Isc=[500.125,495.775,106.526] #moment of inertia of spacecraft
L_cm = 0.9573 #[m]
#torque on the solar array
Tx=TorqueSC*np.cos(np.deg2rad(10))*np.cos(np.deg2rad(63))
Ty=TorqueSC*np.cos(np.deg2rad(10))*np.cos(np.deg2rad(27))
Tz=TorqueSC*np.cos(np.deg2rad(80)) #acting upwards

#decomposate force in function of direction of max torque and adjust for opposite direction due to being reactions
TorqueSAx=Tx*(Isa[0])/(Isc[0])
TorqueSAy=Ty*(Isa[1])/(Isc[1])
TorqueSAz=Tz*(Isa[2])/(Isc[2])


#find corresponding Force
R_y=TorqueSAz/L_cm
R_z=-TorqueSAy/L_cm
#Moments
M_x=TorqueSAx
F_launch = np.array([0, R_y, R_z])
M_launch = np.array([M_x,0,0])
print(F_launch)
print(M_launch)

