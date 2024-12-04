import math

# Input parameters not depending on material
F_yi = 150000.0  # [N]
D_fi = 0.03  # [m]
tau_backup_yield = 122e6  # [Pa]
tau_vehicle_yield = 122e6  # [Pa]
safety_factor = 1.5  # [~]

#materials depending inputs
def findMinimumThickness(F_yi, D_fi):
# minimum thickness backup wall (t2)
    t2_min = F_yi / (math.pi * D_fi * (tau_backup_yield / safety_factor))

# minimum thickness vehicle wall (t3)
    t3_min = F_yi / (math.pi * D_fi * (tau_vehicle_yield / safety_factor))
    return t2_min, t3_min
# Output the results
# print(f"Minimum backup wall thickness (t2): {t2_min:.6f} m")
# print(f"Minimum vehicle wall thickness (t3): {t3_min:.6f} m")