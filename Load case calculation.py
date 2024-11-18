import numpy as np
lat = 0.5 #[g]
lon = 5 #[g]
weight= ((9.03)/2)*9.81 #[N]
L_cm = 1 #[m]
g=9.81 #[m/s^2]
#F_x
R_x=-lat*g #[N]
#M_x
M_x=-L_cm*lat*g #[N]
#F_y
R_y=-lat*g #[N]
#M_y

#F_z
R_z=-lon*g #[N]

