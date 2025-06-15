import numpy as np
from scipy.constants import e, m_u, c

# Constants
amu = m_u  # atomic mass unit in kg
q_e = e    # elementary charge in C

# Beam parameters
Z = 8       # charge number for Ar8+
A = 40      # mass number for Argon
T_keV_u = 10  # kinetic energy per nucleon in keV/u
    
# Convert to SI units
T_joule = T_keV_u * 1e3 * q_e * A  # Total kinetic energy in joules

# Total mass
mass = A * amu  # in kg
    
# Relativistic velocity
gamma = 1 + T_joule / (mass * c**2)
beta = np.sqrt(1 - 1 / gamma**2)
v = beta * c

# Momentum
p = mass * v  # in kg*m/s

# Ra value (all 0.06 m)
Ra = 0.06  # in meters


def compute_brho(keV_per_u, Z, A):
    Ek_joule = keV_per_u * 1e3 * e * A
    mass = A * amu
    gamma = 1 + Ek_joule / (mass * c**2)
    beta = np.sqrt(1 - 1 / gamma**2)
    p = gamma * mass * beta * c  # momentum in kg·m/s
    return p / (Z * e)  # in T·m

def dipole_properties(rbend_cm, theta_deg, brho):
    rbend_m = rbend_cm / 100.0
    theta_rad = np.deg2rad(theta_deg)
    length_m = rbend_m * np.abs(theta_rad)
    B = brho / rbend_m
    return length_m, B

brho = compute_brho(T_keV_u, Z, A)

# Track dipole
rbend_cm = 40.0
theta_deg = -90  # bending to left

rbend_cm = 65
theta_deg = -90
length, B = dipole_properties(rbend_cm, theta_deg, brho)

print(f"Computed Dipole Properties:")
print(f"  Bρ = {brho:.6e} T-m")
print(f"  B  = {B:.6f} T")
print(f"  Effective arc length = {length:.4f} m")
print (B)

