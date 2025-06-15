import numpy as np
import pandas as pd
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

print (p, p / (Z * e))
# Ra value (all 0.06 m)
Ra = 0.06  # in meters

# Electrostatic quads data (name, Vf [V])
equads = {
    "equad1": -8149.25,
    "equad2": 14201.69,
    "equad3": -7506.06,
    "equad4": 6905.82,
    "equad5": -5024.29,
    "equad6": -3067.63,
    "equad7": -8366.68,
    "equad8": 16039.08,
    "equad9": -9579.69,
    "equad10": 11452.67104,
    "equad11": -11905.17808,
    "equad12": -1200.79773,
    "equad13": 1300.45883,
    "equad14": -4086.62666,
    "equad15": 6682.25124,
    "equad16": -15798.80806,
    "equad17": 17848.93706
}

# Compute k1 for each
results = []
for name, Vf in equads.items():
    G = Vf / Ra**2  # electric field gradient [V/m^2]
    Fx = Z * q_e * G * Ra  # Force at x = Ra
    k1 = Fx / (p * v * Ra)  # from F = -k1 * p * v * x
    results.append((name, Vf, G, k1))

# Convert to DataFrame for display
df = pd.DataFrame(results, columns=["Name", "Vf (V)", "G (V/m^2)", "k1 (1/m^2)"])

print(df["k1 (1/m^2)"])
