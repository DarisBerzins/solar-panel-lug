import numpy as np


def moi(m_panel, dim, thick, com_p, com_sc):
    # convert COM coordinates to meters
    com_panel_m = np.array(com_p) / 1000 
    com_spacecraft_m = np.array(com_sc) / 1000 

    # distance between COMs
    d = com_panel_m - com_spacecraft_m  # Component distances (dx, dy, dz)

    # moments of inertia for the solar panel about its own COM
    a, b, t = dim["a"], dim["b"], thick
    i_p_xx = (1 / 12) * m_panel * (b**2 + t**2)
    i_p_yy = (1 / 12) * m_panel * (a**2 + t**2)
    i_p_zz = (1 / 12) * m_panel * (a**2 + b**2)

    # parallel axis theorem 
    i_tot_xx = i_p_xx + m_panel * d[0]**2
    i_tot_yy = i_p_yy + m_panel * d[1]**2
    i_tot_zz = i_p_zz + m_panel * d[2]**2

    return i_tot_xx, i_tot_yy, i_tot_zz


mass_panel = 5.515  # kg
dimensions = {"a": 1.0, "b": 1.85}  # m
thickness = 0.025  # m
com_panel = [-1711.814, -531.825, 159.733]  # mm
com_spacecraft = [-1637.151, 1346.898, 837.037]  # mm

# moments of inertia
I_total_xx, I_total_yy, I_total_zz = moi(
    mass_panel, dimensions, thickness, com_panel, com_spacecraft
)

# results
print(f"Moments of Inertia about the spacecraft COM:")
print(f"Ixx: {I_total_xx:.5f}")
print(f"Iyy: {I_total_yy:.4f}")
print(f"Izz: {I_total_zz:.5f}")
