import numpy as np
import time

# Calculation of the total force
def get_P(F1, Fy, Fz):  # vectors
    P = F1 + Fy + Fz
    return P


def Area_Aav(w, D, t):
    A1 = (w / 2 - D / 2 * np.cos(np.pi / 4)) * t
    A4 = A1
    A2 = (w / 2 - D / 2) * t
    e = w / 2
    A3 = (e - D / 2) * t
    Aav = 6 / (3 / A1 + 1 / A2 + 1 / A3 + 1 / A4)
    return Aav


def compute_Kt_material1(WD):
    # Data points for W/D and Kt
    data_points = [
        (1, 1),
        (1.5, 0.96),
        (3, 0.92),
        (3.5, 0.908),
        (3.9, 0.9),
        (4.2, 0.88),
        (4.4, 0.86),
        (4.6, 0.84),
        (4.8, 0.8),
        (4.9, 0.76)
    ]

    # Sort data_points by W/D in case they're not sorted
    data_points.sort()

    # Handle edge cases
    if WD <= data_points[0][0]:
        return data_points[0][1]
    if WD >= data_points[-1][0]:
        return data_points[-1][1]

    # Linear interpolation
    for i in range(len(data_points) - 1):
        WD_i, Kt_i = data_points[i]
        WD_next, Kt_next = data_points[i + 1]

        if WD_i <= WD <= WD_next:
            # Linear interpolation formula
            return Kt_i + (Kt_next - Kt_i) / (WD_next - WD_i) * (WD - WD_i)
            # return 0.9
    # If WD is outside the range, return None (this shouldn't happen with edge cases handled)
    return None


def compute_Kt_material2(WD):
    # Data points for W/D and Kt for Curve 3
    data_points = [
        (1, 1),
        (2, 0.94),
        (3, 0.87),
        (4, 0.82),
        (5, 0.74)
    ]

    # Sort data_points by W/D in case they're not sorted
    data_points.sort()

    # Handle edge cases
    if WD <= data_points[0][0]:
        return data_points[0][1]
    if WD >= data_points[-1][0]:
        return data_points[-1][1]

    # Linear interpolation
    for i in range(len(data_points) - 1):
        WD_i, Kt_i = data_points[i]
        WD_next, Kt_next = data_points[i + 1]

        if WD_i <= WD <= WD_next:
            # Linear interpolation formula
            return Kt_i + (Kt_next - Kt_i) / (WD_next - WD_i) * (WD - WD_i)

    # If WD is outside the range, return None (this shouldn't happen with edge cases handled)
    return None


def compute_K_b_material12(eD):  # the same for both materials
    # Data points for e/D and K_br
    data_points = [
        (0.5, 0),
        (1, 0.85),
        (1.3, 1.1),
        (1.9, 1.45),
        (2.2, 1.55)
    ]

    # Sort data_points by e/D in case they're not sorted
    data_points.sort()

    # Handle edge cases
    if eD <= data_points[0][0]:
        return data_points[0][1]
    if eD >= data_points[-1][0]:
        return data_points[-1][1]

    # Linear interpolation
    for i in range(len(data_points) - 1):
        eD_i, K_br_i = data_points[i]
        eD_next, K_br_next = data_points[i + 1]

        if eD_i <= eD <= eD_next:
            # Linear interpolation formula
            return K_br_i + (K_br_next - K_br_i) / (eD_next - eD_i) * (eD - eD_i)

    # If eD is outside the range, return None (this shouldn't happen with edge cases handled)
    return None


def compute_K_tu_material2(A_av_A_br):
    # Data points for A_av/A_br and K_tu
    data_points = [
        (0, 0),
        (0.1, 0.11),
        (0.2, 0.21),
        (0.3, 0.33),
        (0.4, 0.45),
        (0.5, 0.55),
        (0.6, 0.64),
        (0.7, 0.73),
        (0.8, 0.81),
        (0.9, 0.88),
        (1.0, 0.94),
        (1.1, 1.0),
        (1.2, 1.05),
        (1.3, 1.09),
        (1.4, 1.1)
    ]

    # Sort data_points by A_av/A_br in case they're not sorted
    data_points.sort()

    # Handle edge cases
    if A_av_A_br <= data_points[0][0]:
        return data_points[0][1]
    if A_av_A_br >= data_points[-1][0]:
        return data_points[-1][1]

    # Linear interpolation
    for i in range(len(data_points) - 1):
        A_av_A_br_i, K_tu_i = data_points[i]
        A_av_A_br_next, K_tu_next = data_points[i + 1]

        if A_av_A_br_i <= A_av_A_br <= A_av_A_br_next:
            # Linear interpolation formula
            return K_tu_i + (K_tu_next - K_tu_i) / (A_av_A_br_next - A_av_A_br_i) * (A_av_A_br - A_av_A_br_i)

    # If A_av_A_br is outside the range, return None (this shouldn't happen with edge cases handled)
    return None


def compute_K_tu_material1(A_av_A_br):
    # Data points for A_av/A_br and K_tu
    data_points = [
        (0, 0),
        (0.1, 0.12),
        (0.2, 0.25),
        (0.3, 0.37),
        (0.4, 0.49),
        (0.5, 0.56),
        (0.6, 0.6),
        (0.7, 0.63),
        (0.8, 0.65),
        (0.9, 0.66),
        (1.0, 0.67),
        (1.1, 0.67),
        (1.2, 0.68),
        (1.3, 0.68),
        (1.4, 0.68)
    ]

    # Sort data_points by A_av/A_br in case they're not sorted
    data_points.sort()

    # Handle edge cases
    if A_av_A_br <= data_points[0][0]:
        return data_points[0][1]
    if A_av_A_br >= data_points[-1][0]:
        return data_points[-1][1]

    # Linear interpolation
    for i in range(len(data_points) - 1):
        A_av_A_br_i, K_tu_i = data_points[i]
        A_av_A_br_next, K_tu_next = data_points[i + 1]

        if A_av_A_br_i <= A_av_A_br <= A_av_A_br_next:
            # Linear interpolation formula
            return K_tu_i + (K_tu_next - K_tu_i) / (A_av_A_br_next - A_av_A_br_i) * (A_av_A_br - A_av_A_br_i)

    # If A_av_A_br is outside the range, return None (this shouldn't happen with edge cases handled)
    return None


'''
load_cases = [
    {"case": 1, "Fx": -4.905 * np.array([1, 0, 0]), "Fy": -4.905 * np.array([0, 1, 0]), "Fz": -58.86 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 2, "Fx": 4.905 * np.array([1, 0, 0]), "Fy": 4.905 * np.array([0, 1, 0]), "Fz": -58.86 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 3, "Fx": 19.62 * np.array([1, 0, 0]), "Fy": 19.62 * np.array([0, 1, 0]), "Fz": -34.335 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 4, "Fx": 19.62 * np.array([1, 0, 0]), "Fy": 19.62 * np.array([0, 1, 0]), "Fz": 14.715 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 5, "Fx": 4.905 * np.array([1, 0, 0]), "Fy": 4.905 * np.array([0, 1, 0]), "Fz": 19.62 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 6, "Fx": -4.905 * np.array([1, 0, 0]), "Fy": -4.905 * np.array([0, 1, 0]), "Fz": 19.62 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 7, "Fx": -19.62 * np.array([1, 0, 0]), "Fy": -19.62 * np.array([0, 1, 0]), "Fz": 14.715 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 8, "Fx": -19.62 * np.array([1, 0, 0]), "Fy": -19.62 * np.array([0, 1, 0]), "Fz": -34.335 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])},
    {"case": 9, "Fx": -19.62 * np.array([1, 0, 0]), "Fy": -19.62 * np.array([0, 1, 0]), "Fz": -34.335 * np.array([0, 0, 1]), "F1": np.array([0, 0, 0])}, #to be changed
    {"case": 10, "deployment": "Main thruster", "Fx": -2.899347 * np.array([1, 0, 0]), "Fy": np.array([0, 0, 0]), "Fz": np.array([0, 0, 0]), "F1": np.array([0, 0, 0])},
]
'''
# these still have to be decided
SF = SF_yield = SF_bearing = 1  #

# for the chosen loadcase
# Newtons


Fx = np.multiply(np.array([511, 0, 0]), SF)
Fy = np.multiply(np.array([0, 108, 0]), SF)
Fz = np.multiply(np.array([0, 0, -324.6]), SF)
F1 = np.multiply(np.array([0, 0, 0]), SF)

P = get_P(F1, Fy, Fz)
# *0.225
P_axial = np.dot(P, [0, 1, 0])
P_transverse = np.dot(P, [0, 0, 1])

materials = [
    {"number": 1, "name": "Aluminum 7075", "Ftu": 524 * (10 ** 6)  # Pa
     # *145.038
     },
    {"number": 2, "name": "Aluminum 2024-T4", "Ftu": 469 * (10 ** 6)  # Pa
     # *145.038

     }]

# Only material 2
# materials = [
#     {"number": 2, "name": "Aluminum 2024-T4", "Ftu": 469 * (10 ** 6)  # Pa
#      # *145.038
#
#      }]
'''
materials = [
    {"number":1, "name": "Aluminum 7075", "Ftu": 524*145.038#Psi
    },
    {"number":2, "name": "Aluminum 2024-T4", "Ftu": 469*145.038#Psi
    }]
'''


# Initialize geometrical parameters


# Material properties (example values, adapt as needed)

# Calculate axial and transverse components of the load
# Function to calculate R_a and R_tr
def calculate_R_values(material, D1, t1, w):
    Ftu = material["Ftu"]

    if D1 >= w:
        return 42, 69
    At = (w - D1) * t1  # Axial area
    Abr = D1 * t1  # Bearing area
    Aav = Area_Aav(w, D1, t1)
    if material["number"] == 1:
        Kt = compute_Kt_material1(w / D1)  # Kt as a function of material and w/D1
        Kb = compute_K_b_material12((w / 2) / D1)  # Kb as a function and e/D1 (and maybe D/t)
        Ktu = compute_K_tu_material1(Aav / Abr)  # Ktu as a function of material and A_av/A_br
    else:
        Kt = compute_Kt_material2(w / D1)
        Kb = compute_K_b_material12((w / 2) / D1)
        Ktu = compute_K_tu_material2(Aav / Abr)

    # Calculate P values
    # !!! check the scaling factor!!!***
    Pu = Kt * Ftu * At  # Equation (6)
    Pbru = Kb * Ftu * Abr  # Equation (7)
    Ptu = Ktu * Abr * Ftu  # Equation (10)
    Ra = P_axial / min(Pu, Pbru)
    Rtr = P_transverse / Ptu
    return Ra, Rtr

best_deviation = [10000, None, None, None, None]
safety_margin = 0

best_deviation = [0.8, 0.022,  0.005, 0.02, 2]

# for material in materials:
#     for D1 in np.arange(0.02, 0.5, 0.001): # meters
#         for i in range(100):
#             print("-", end = ""),
#         print()
#         print("X", end = ""),
#         for i in range(int(100*((D1.item()-0.003)/0.5))):
#             print("X", end = ""),
#         print()
#         for i in range(100):
#             print("-", end = ""),
#         print()
#         print("Material: " + str(material["number"]))
#         print("Progress: " + str(((D1.item()-0.003)/0.5)*100) + "%")
#         print("Best fit: " + str(best_deviation[0]))
#         print("Safety margin: " + str(safety_margin))
#         print()
#         print("Best w, t1, D1, material: " + str(best_deviation[1]) + ',' + str(best_deviation[2]) + ',' + str(best_deviation[3]) + ',' + str(best_deviation[4]))
#         print()
#         print("Trying D = " + str(D1))
#         print()
#         for t1 in np.arange(0.001, 0.01, 0.001):
#             # print(D1, t1)
#             for w in np.arange(D1, 0.5, 0.002):  # w> t1 >e (doesn't) affect the weight> D ( a higher value affect the weight positivily), therefore check e at the end
#                 Ra, Rtr = calculate_R_values(material, D1, t1, w)
#                 # print(Ra, Rtr)
#                 # print(Ra,Rtr)
#                 # print(np.pow(Ra,1.6),np.pow(abs(Rtr),1.6))
#                 #deviation = 1 - (np.pow(Ra, 1.6) + np.pow(abs(Rtr), 1.6))
#                 deviation = 1 - (np.power(Ra, 1.6) + np.power(abs(Rtr), 1.6))
#                 if deviation < best_deviation[0] and deviation > 0:
#                     best_deviation = [deviation, w, t1, D1, material["number"]]
#                     safety_margin = (1/np.pow((np.pow(Ra,1.6) + np.pow(abs(Rtr), 1.6)), 0.625)) -1
#                     # print(best_deviation)
#                     # time.sleep(1)
#                 # if deviation < 0.5 and deviation > 0:
#                 #     print(material["name"], D1, t1, w)
#     for i in range(100):
#         print("-", end = ""),
#     print()
#     print("X", end = ""),
#     for i in range(int(100*((D1.item()-0.03)/0.5))):
#         print("X", end = ""),
#     print()
#     for i in range(100):
#         print("-", end = ""),
#     print()
#     print("Material: " + str(material["number"]))
#     print("Progress: " + str(((D1.item()-0.03)/0.5)*100) + "%")
#     print("Best fit: " + str(best_deviation[0]))
#     print("Safety margin: " + str(safety_margin))
#     print()
#     print("Best w, t1, D1, material: " + str(best_deviation[1]) + ',' + str(best_deviation[2]) + ',' + str(best_deviation[3]) + ',' + str(best_deviation[4]))
#     print()
#     print("Trying D = " + str(D1))
#     print()
# # Output the best design '''