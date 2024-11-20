import numpy as np

# Calculation of the total force
def get_P (F1, Fy, Fz): #vectors
    P=F1+Fy+Fz
    return P


def Area_Aav (w, D, e, t):
    A1=(w/2-D/2*np.cos(np.pi/4))*t
    A4=A1
    A2=(w/2-D/2)*t
    A3=(e-D/2)*t
    Aav=6/(3/A1+1/A2+1/A3+1/A4)
    return Aav

materials = [
    {"name": "Aluminum 7075", "Ftu": 524},
    {"name": "Aluminum 2024-T4", "Ftu": 469}]

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


# Material properties (example values, adapt as needed)

P=get_P(F1,Fy,Fz) #divide by two in case of using two flanges

# Calculate axial and transverse components of the load
P_axial = np.dot(P,[0,1,0])
P_transverse=np.dot(P,[0,0,1])
# Function to calculate R_a and R_tr
def calculate_ratios(material, D1, t1, w, e):

    Ftu = material["Ftu"]

    At = (w - D1) * t1  # Axial area
    Abr = D1 * t1  # Bearing area
    Aav=Area_Aav(w,D1,e,t1)

    Kt=1#Kt as a function of material and w/D1
    Kb=1#Kb as a function and e/D1 (and maybe D/t)
    Ktu=1#Ktu as a function of material and A_av/A_br



    # Calculate P values
    Pu = Kt * Ftu * At  # Equation (6)
    Pbru = Kb * Ftu * Abr  # Equation (7)
    Ptu = Ktu * Abr * Ftu  # Equation (10)

    # Calculate R_a and R_tr
    Ra = P_axial / min(Pu, Pbru)
    Rtr = P_transverse / Ptu

    return Ra, Rtr

# Iterate over materials and geometries to minimize |R_a + R_tr - 1|
best_design = None
min_deviation = float('inf')

for material in materials:
    for D1 in [0.01, 0.015, 0.02, 0.025]: #choose this range s.t. the differences can be properly manufactured
        for t1 in [0.005, 0.01, 0.015]:
            for w in [0.03, 0.05, 0.07]:
                Ra, Rtr = calculate_ratios(material, D1, t1, w)
                deviation = abs((Ra^1.6 + Rtr^1.6) - 1)

                if deviation < min_deviation:
                    min_deviation = deviation
                    best_design = {
                        "material": material["name"],
                        "D1": D1,
                        "t1": t1,
                        "w": w,
                        "Ra": Ra,
                        "Rtr": Rtr,
                        "deviation": deviation,
                    }

# Output the best design
if best_design:
    print("Best Design Found:")
    print(f"Material: {best_design['material']}")
    print(f"D1: {best_design['D1']} m")
    print(f"t1: {best_design['t1']} m")
    print(f"w: {best_design['w']} m")
    print(f"R_a: {best_design['Ra']:.3f}")
    print(f"R_tr: {best_design['Rtr']:.3f}")
    print(f"Deviation: {best_design['deviation']:.5f}")
else:
    print("No feasible design found.")