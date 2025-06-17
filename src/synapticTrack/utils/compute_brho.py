import numpy as np
from scipy.constants import *

# Physical constants
#c,  speed of light in m/s
#e,  elementary charge in C
#u,  atomic mass unit in kg
eV_to_kgms = e / c  # 1 eV/c in kg*m/s

def compute_beam_momentum_brho(kinetic_energy_keVu, charge_number, mass_number):
    """
    Compute relativistic momentum (eV/c, kg·m/s) and Brho (T·m) from beam parameters.
    
    Parameters:
        kinetic_energy_keVu: kinetic energy in keV/u
        charge_number: ion charge state (e.g., 8 for Ar8+)
        mass_number: atomic mass number (e.g., 40 for Argon-40)
    
    Returns:
        dict: momentum_eVc, momentum_kgms, brho_Tm
    """
    # Convert energies
    kinetic_energy_MeV = kinetic_energy_keVu * 1e-3 * mass_number  # total kinetic energy in MeV
    rest_energy_MeV = mass_number * 931.494  # rest mass energy in MeV
    total_energy_MeV = kinetic_energy_MeV + rest_energy_MeV
    
    # Gamma and beta
    gamma = total_energy_MeV / rest_energy_MeV
    beta = np.sqrt(1 - 1 / gamma**2)
    
    # Relativistic momentum in MeV/c
    momentum_MeVc = gamma * beta * rest_energy_MeV
    momentum_eVc = momentum_MeVc * 1e6  # convert to eV/c
    momentum_kgms = momentum_eVc * eV_to_kgms
    
    # Magnetic rigidity Brho = p / (q * c)
    Brho_Tm = momentum_kgms / (charge_number * e)
    
    return {
        "momentum_MeV/c": momentum_MeVc,
        "momentum_kgm/s": momentum_kgms,
        "Brho_Tm": Brho_Tm
    }

