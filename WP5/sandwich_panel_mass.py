nomex_rho = 48.2  # kg/m^3
weavefabric_rho = 1611  # kg/m^3
fabric_t = 0.00019805  # m
nomex_t = 0.015  # m
area = 1.0  # m^2

mass_panel = 2 * (fabric_t * area) * weavefabric_rho + (nomex_t * area) * nomex_rho

print(mass_panel, "kg")
