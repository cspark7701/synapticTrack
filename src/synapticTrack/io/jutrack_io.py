import pandas as pd
import numpy as np
from scipy.constants import c, physical_constants
from typing import Union
from os.path import basename, splitext

from synapticTrack.beam import Beam, BeamWS, BeamAS

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

class JuTrackIO:
    @staticmethod
    def read(filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
        particles = np.loadtxt(filename)
        return JuTrackIO.convert(particles, mass_number, charge_state, beam_current, reference_energy)

    @staticmethod
    def convert(particles: np.ndarray, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
        x, px_p0, y, py_p0, z, delta = particles.T
        E0 = mass_number * amu
        gamma0 = 1 + reference_energy / amu
        beta0 = np.sqrt(1 - 1 / gamma0**2)
        p0 = gamma0 * beta0 * E0
        p_total = p0 * (1 + delta)
        gamma = np.sqrt(1 + (p_total / E0)**2)
        dW = (gamma - gamma0) * amu
        pz_p0 = np.sqrt((1 + delta)**2 - px_p0**2 - py_p0**2)
        xp = (px_p0 / pz_p0) * 1e3       # mrad
        yp = (py_p0 / pz_p0) * 1e3       # mrad
        x_mm = x * 1e3                   # mm
        y_mm = y * 1e3                   # mm
        dt = -z / (beta0 * c)
        df = pd.DataFrame({"x": x_mm, "xp": xp, "y": y_mm, "yp": yp, "dt": dt, "dW": dW})
        return Beam(df, mass_number, charge_state, beam_current, reference_energy)

    @staticmethod
    def write(filename: str, beam: Beam):
        x = beam.state['x'].values * 1e-3
        y = beam.state['y'].values * 1e-3
        xp = beam.state['xp'].values * 1e-3
        yp = beam.state['yp'].values * 1e-3
        dt = beam.state['dt'].values
        dW = beam.state['dW'].values
        E0 = beam.mass_number * amu
        gamma0 = 1 + beam.reference_energy / amu
        beta0 = np.sqrt(1 - 1 / gamma0**2)
        p0 = gamma0 * beta0 * E0
        kinetic = beam.reference_energy + dW
        gamma = 1 + kinetic / amu
        beta = np.sqrt(1 - 1 / gamma**2)
        p = gamma * beta * E0
        delta = (p - p0) / p0
        px_p0 = xp
        py_p0 = yp
        pz_p0 = np.sqrt((1 + delta)**2 - px_p0**2 - py_p0**2)
        px_p0 = xp * pz_p0
        py_p0 = yp * pz_p0
        z = -beta0 * c * dt
        df = pd.DataFrame({"x": x, "px_p0": px_p0, "y": y, "py_p0": py_p0, "z": z, "delta": delta})
        df.to_csv(filename, sep=' ', header=False, index=False, float_format='%.12e')

    def convert_to_jutrack_coordinates(beam) -> pd.DataFrame:
        """
        Converts a DataFrame of beam coordinates from synapticTrack to JuTrack format.
        
        Args:
            beam (Beam): synapticTrack beam object
            
        Returns:
            pd.DataFrame: Converted coordinates in JuTrack format.
        """
        # Convert position units: mm -> m
        x = beam.state['x'].values * 1e-3
        y = beam.state['y'].values * 1e-3

        # Convert angles from mrad to rad
        xp = beam.state['xp'].values * 1e-3
        yp = beam.state['yp'].values * 1e-3

        dt = beam.state['dt'].values
        dW = beam.state['dW'].values

        # Reference mass and energy
        E0 = beam.mass_number * amu                    # total rest mass energy in MeV
        gamma0 = 1 + beam.reference_energy / amu
        beta0 = np.sqrt(1 - 1 / gamma0**2)
        p0 = gamma0 * beta0 * E0  # Reference momentum [MeV/c]

        # Actual energy
        kinetic_energy = beam.mass_number * (beam.reference_energy + dW)  # MeV/u
        gamma = 1 + kinetic_energy / E0
        beta = np.sqrt(1 - 1 / gamma**2)
        p = gamma * beta * E0         # MeV/c

        delta = (p - p0) / p0

        # Initial px/p0, py/p0 (approximate)
        px_p0 = xp
        py_p0 = yp

        # Enforce longitudinal momentum constraint
        pz_p0 = np.sqrt((1 + delta)**2 - px_p0**2 - py_p0**2)
        #pz_p0 = np.sqrt(np.clip((1 + delta)**2 - px_p0**2 - py_p0**2, epsilon, None))

        # Now refine px/p0 and py/p0 using better scaling with pz
        px_p0 = xp * pz_p0
        py_p0 = yp * pz_p0

        # z coordinate in JuTrack: -βc dt
        z = - beta0 * c * dt
        # Compose DataFrame
        jutrack_df = pd.DataFrame({
            "x": x,
            "px_p0": px_p0,
            "y": y,
            "py_p0": py_p0,
            "z": z,
            "delta": delta
        })

        return jutrack_df
