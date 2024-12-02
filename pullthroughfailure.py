import math

#input parameters
F_yi = 150000.    #[N]
D_fi = 0.015    #[m]
D_fo = 0.02    #[m]
t_2 = 0.01     #[m]  
t_3 = 0.01    #[m]  
tau_backup_yield = 167.e6 #[Pa]
tau_vehicle_yield = 167.e6 #[Pa]
sigma_yield = 290.e6 #[Pa]
safety_factor = 1.5 #[~]

#functions
def calculate_A_shear(D, t):
    area_shear = math.pi * D * t
    return area_shear

def calculate_A_normal(D_o, D_i):
    area_normal = (D_o*2 - D_i*2) * math.pi / 4
    return area_normal

def stress_yield_checking(stress, stress_yield, safety = 1.5):
    okay = 1
    if safety * stress > stress_yield:
        okay = 0
    return okay
    
def print_okay(good, stress_okay, stress_yield_okay, safety2 = 1.5):
    message = ""
    if good == 1:
        message = "does not yield because of"
    if good == 0:   
        difference_needed = str(round((stress_yield_okay/safety2 - stress_okay)/(-10e6),3))
        message = "will fail, reduce the stress with " + difference_needed + "[MPa]"
    return message

    
#computations lug backup wall 
A_shear_backup = calculate_A_shear(D_fi, t_2)
tau_backup = F_yi / A_shear_backup

#computations vehicle wall
A_shear_vehicle = calculate_A_shear(D_fi, t_3)
tau_vehicle = F_yi / A_shear_vehicle

#computations normal stress
A_normal = calculate_A_normal(D_fo, D_fi)
sigma = F_yi / A_normal 

#checking for yielding
    #backup
okay_backup = stress_yield_checking(tau_backup, tau_backup_yield, safety_factor)
message_backup = print_okay(okay_backup, tau_backup, tau_backup_yield, safety_factor)

    #vehicle
okay_vehicle = stress_yield_checking(tau_vehicle, tau_vehicle_yield, safety_factor)
message_vehicle = print_okay(okay_vehicle, tau_vehicle, tau_vehicle_yield, safety_factor)

    #normal stress
okay_normal = stress_yield_checking(sigma, sigma_yield, safety_factor)
message_normal = print_okay(okay_normal, sigma, sigma_yield, safety_factor)

#printing
print("The backup wall " + message_backup + " shear stress.")
print("The vehicle wall " + message_vehicle + " shear stress.")
print("The lunge " + message_normal + " normal stress.")