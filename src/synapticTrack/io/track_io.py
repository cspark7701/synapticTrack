import pandas as pd
import numpy as np
from scipy.constants import c, physical_constants
from typing import Union
from os.path import basename, splitext

from synapticTrack.beam import Beam, BeamWS, BeamAS

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

class TrackIO:
    @staticmethod
    def read(filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
        columns = ["Nseed", "iq", "dt", "dW", "x", "xp", "y", "yp"]
        df = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=columns, engine='python')
        df['x'] *= 10  # cm to mm
        df['y'] *= 10
        return Beam(df, mass_number, charge_state, beam_current, reference_energy)

    @staticmethod
    def convert(particles: np.ndarray, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
        Nseed, iq, dt, dW, x, xp, y, yp = particles.T
        df = pd.DataFrame({
            "x": x * 10,
            "xp": xp,
            "y": y * 10,
            "yp": yp,
            "dt": dt,
            "dW": dW
        })
        return Beam(df, mass_number, charge_state, beam_current, reference_energy)

    @staticmethod
    def write(filename: str, beam: Beam):
        df = beam.state.copy()
        df['x'] /= 10
        df['y'] /= 10
        df.insert(0, 'iq', beam.charge_state)
        df.insert(0, 'Nseed', np.arange(len(df)))
        df[['Nseed', 'iq', 'dt', 'dW', 'x', 'xp', 'y', 'yp']].to_csv(
            filename, sep=' ', header=False, index=False, float_format='%.6e')

