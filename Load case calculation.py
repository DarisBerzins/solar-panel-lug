#4.1-4.2
import numpy as np
lat = 2 #[g]
lon = 3.5 #[g]
weight= (4.515+1)*9.81 #[N]
L_cm = 0.9573 #[m]
g=9.81 #[m/s^2]
F_thruster=511


#sum of forces in x
R_x=-lat*g #[N]
#sum of moments in x
M_x=-L_cm*lat*g #[N]
#sum of forces in y
R_y=-lat*g #[N]
#sum of moments in y
M_y=L_cm*lat*g #[N]
#sum of forces in z
R_z=-lon*g #[N]
#sum of moments in z
M_z=0
F_launch = np.array([R_x, R_y, R_z])
M_launch = np.array([M_x, M_y, M_z])

print(F_launch)
print(M_launch)