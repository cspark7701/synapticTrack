import pandas as pd
import numpy as np
from scipy.constants import c, physical_constants
from typing import Union
from os.path import basename, splitext

from synapticTrack.beam import Beam, BeamWS, BeamAS

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

class ScannerIO:
    @staticmethod
    def read_wire_scanner(filename: str) -> BeamWS:
        cols = ["x_pos", "x_current", "y_pos", "y_current", "d_pos", "d_current"]
        df = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=cols, engine='python')
        return BeamWS(df, scan_id=splitext(basename(filename))[0])

    @staticmethod
    def read_allison_scanner(filename: str) -> BeamAS:
        cols = ["x", "xp", "x_current", "hv", "y_current"]
        df = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=cols, engine='python')
        return BeamAS(df, scan_id=splitext(basename(filename))[0])
