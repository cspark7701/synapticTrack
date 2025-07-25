import numpy as np
from synapticTrack.utils.stats import (
    calc_variance, calc_covariance
)
from scipy.constants import c, physical_constants

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

class Twiss:
    def __init__(self, beam):
        """
        Compute Twiss parameters from a Beam object.
        """
        self._beam = beam
        self._twiss_x = self.compute_twiss(beam.x, beam.xp)
        self._twiss_y = self.compute_twiss(beam.y, beam.yp)
        self._twiss_z = self.compute_twiss(beam.dt, beam.dW)

    @staticmethod
    def compute_twiss(u, up):
        """
        Compute emittance and Twiss parameters from 2D phase space projection.

        Returns:
            dict: {emittance, alpha, beta, gamma}

        """
        #from synapticTrack.utils.stats import calc_variance, calc_covariance

        sigma_u = calc_variance(u)
        sigma_up = calc_variance(up)
        sigma_uup = calc_covariance(u, up)

        det = sigma_u * sigma_up - sigma_uup**2
        if det <= 0:
            raise ValueError("Non-physical Twiss parameters: determinant ≤ 0")

        emit = np.sqrt(det)
        beta = sigma_u / emit
        alpha = -sigma_uup / emit
        gamma = sigma_up / emit

        # Optional self-consistency check
        gamma_check = (1 + alpha**2) / beta
        if abs(gamma - gamma_check) > 1e-8:
            print(f"Warning: Inconsistent Twiss gamma in {label} plane. "
                  f"Expected γ={gamma_check:.3f}, got γ={gamma:.3f}")

        return {
            "emittance": emit,
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma
        }

    @property
    def horizontal(self):
        return self._twiss_x

    @property
    def vertical(self):
        return self._twiss_y

    @property
    def longitudinal(self):
        return self._twiss_z

    def values(self):
        """
        Return Twiss parameter dictionary.
        """
        return {
            "twiss_x": self._twiss_x,
            "twiss_y": self._twiss_y,
            "twiss_z": self._twiss_z
        }

    def normalized_emittance(self, plane='x'):
        """
        Compute normalized emittance: ε_n = γ_rel * β_rel * ε
        Args:
            plane (str): 'x', 'y', or 'z'
    
        Returns:
            float: normalized emittance [mm·mrad]
        """
        gamma = 1 + self._beam.reference_energy / amu
        beta = np.sqrt(1 - 1 / gamma**2)

        if plane == 'x':
            unnorm_emit = self._twiss_x['emittance']
        elif plane == 'y':
            unnorm_emit = self._twiss_y['emittance']
        elif plane == 'z':
            unnorm_emit = self._twiss_z['emittance']
        else:
            raise ValueError("plane must be 'x', 'y', or 'z'")

        return (beta * gamma * unnorm_emit)

    def normalized_emittances(self):
        return {k: self.normalized_emittance(k) for k in ['x', 'y', 'z']}


