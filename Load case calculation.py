#4.1-4.2
import numpy as np
lat = 2#[g]
lon = 3.5#[g]
weight= (4.515+1)*9.81 #[N]
mass_sa=4.515+1
L_cm = 0.9573 #[m]
Marm=1.650/2+0.9573 # distance from center of mass solar array and main body
g=9.81 #[m/s^2]
F_thruster=511
#<3
#load case during launch
#sum of forces in x
R_x=-lat*g*mass_sa #[N]
#sum of moments in x
M_x=-L_cm*lat*g*mass_sa #[N]
#sum of forces in y
R_y=-lat*g*mass_sa #[N]
#sum of moments in y
M_y=L_cm*lat*g*mass_sa #[N]
#sum of forces in z
R_z=-lon*g*mass_sa #[N]
#sum of moments in z
M_z=0

F_launch = np.array([R_x, R_y, R_z])
M_launch = np.array([M_x, M_y, M_z])

print(F_launch)
print(M_launch)

#Load case main thruster
#sum of forces in x
R_xt=F_thruster
#sum of moments around z
M_zt=F_thruster*Marm

F_thruster = np.array([R_xt, 0, 0])
M_thruster = np.array([0, 0, M_zt])
print(F_thruster)
print(M_thruster)