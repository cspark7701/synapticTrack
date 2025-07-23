import pandas as pd
import numpy as np
from scipy.constants import c, physical_constants
from typing import Union
from os.path import basename, splitext

from synapticTrack.beam import Beam, BeamWS, BeamAS

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

class OPALIO:
    @staticmethod
    def read(filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
        particles = np.loadtxt(filename)
        return TrackIO.convert(particles, mass_number, charge_state, beam_current, reference_energy)

    @staticmethod
    def write(filename: str, beam: Beam):
        beam.state.to_csv(filename, sep=' ', header=True, index=False)
