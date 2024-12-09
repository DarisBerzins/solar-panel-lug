import numpy as np

# Inputs (replace with actual values)
F_y = 0 # Axial force along Y (N)
F_x =  # Axial force along X (N)
F_z = 189 # Axial force along Z (N)
d   = 0.00325  # Moment arm   
M_f_x = -F_x*d # Moment due to X force (Nm)
M_f_z = F_z*d # Moment due to Z force (Nm)
m_z = 103  # Moment about Z-axis (Nm)
m_x = 103  # Moment about X-axis (Nm)
M_z = M_f_x + m_z # Total Moment about Z-axis (Nm)
M_x = M_f_z + m_x # Total Moment about X-axis (Nm)
n_f = 4    # Number of fasteners
coordinates = [(0.00425, 0.001075), (0.00425, -0.001075), (-0.00425, 0.001075), (-0.00425, -0.001075)]  # Fastener (x, y) coordinates (m)
t = 0.02   # Thickness of attached part (m)
D_fo = 0.02  # Outer diameter of fastener head (m)
R_fo = D_fo / 2  # Outer radius of fastener head (m)
D_fi = 0.015  # Inner diameter of fastener (m)
R_fi = D_fi / 2  # Inner radius of fastener head (m)
sigma_yield = 222e6  # Yield stress of material (Pa)

# Step 1: Calculate CG of the fastener pattern
x_coords, y_coords = zip(*coordinates)
x_cg = sum(x_coords) / n_f  # CG in x-direction
y_cg = sum(y_coords) / n_f  # CG in y-direction

# Step 2: Calculate radial distances and their effects
radii_squared_sum = sum((x - x_cg)**2 + (y - y_cg)**2 for x, y in coordinates)

# Step 3: Calculate loads on fasteners
F_pz = F_y / n_f  # Force distributed equally along the Y-axis

# Initialize the list for total loads
F_yi = []

for x, y in coordinates:
    # Contributions from M_z
    Mz_contribution = M_z * (x - x_cg) / radii_squared_sum
    
    # Contributions from M_x
    Mx_contribution = M_x * (y - y_cg) / radii_squared_sum
    
    # Total out-of-plane force for this fastener
    F_total = F_pz + Mz_contribution + Mx_contribution
    F_yi.append(F_total)

# Step 4: Stress calculations
cross_section_area = np.pi * (R_fo**2 - R_fi**2)  # Cross-sectional area of fastener
normal_stresses = [F / cross_section_area / t for F in F_yi]

# Step 5: Margins of Safety
margins_of_safety = [(sigma_yield / sigma - 1) for sigma in normal_stresses]

# Output results
print("Results for Fastener Loading:")
for i, (stress, ms, Fyi) in enumerate(zip(normal_stresses, margins_of_safety, F_yi)):
    status = "Tension" if Fyi > 0 else "Compression"
    print(f"Fastener {i+1}:")
    print(f"  Out-of-Plane Load (F_yi): {Fyi:.2f} N ({status})")
    print(f"  Normal Stress: {stress:.2e} Pa")
    print(f"  Margin of Safety: {ms:.2f}")
    print()

# Step 6: Check for failure
failures = [i+1 for i, ms in enumerate(margins_of_safety) if ms < 0]
if failures:
    print(f"Design failing for fastener(s): {failures}. Consider increasing t or using stronger material.")
else:
    print("Design is safe.")
