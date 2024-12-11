
#load case calculation slew
Isc=[500.125,495.775,106.526] #moment of inertia of spacecraft
L_cm = 0.9573 #[m]
TorqueSC= 75 #[Nm]
#==============================================
#load case calculation
lat = 2 #[g]
lon = 3.5 #[g]
weight= (4.515+1)*9.81 #[N]
L_cm = 0.9573 #[m]
g=9.81 #[m/s^2]
F_thruster=511
#===============================================
#lug design
# Input parameters
Fx = 500  # Force in x direction (N)
Fy = 300  # Force in y direction (N)
Fz = 400  # Force in z direction (N)
F1 = 300  # Force in z direction (N)
SF_yield = 1.5 # these still have to be decided
SF_bearing = 1.5#

# Initialize geometrical parameters
D1 = 0.02  # Initial guess for hole diameter (m)
t1 = 0.01  # Initial guess for lug thickness (m)
w = 0.05   # Initial guess for lug width (m)
e = 0.03   # Initial guess for edge distance (m)

materials = [
    {"name": "Aluminum 7075", "Ftu": 524},
    {"name": "Aluminum 2024-T4", "Ftu": 469}]

#===================================================
#pull-through failure
safety_factor = 1.5  # [~]

#===================================================
#moment of inertia of solar array
mass_panel = 5.515  # kg
dimensions = {"a": 1.0, "b": 1.85}  # m
thickness = 0.025  # m
com_panel = [-1711.814, -531.825, 159.733]  # mm
com_spacecraft = [-1637.151, 1346.898, 837.037]  # mm

#=======================================================
#thermal stress check
maxSolarPanelTemperature = 383.15#in Kelvins
minSolarPanelTemperature = 168.15#in Kelvins
assemblyReferenceTemperature = 288.15#in Kelvins

#=======================================================
#Fasterners design

fastener_horizontal_spacing = 0.2 # Meters