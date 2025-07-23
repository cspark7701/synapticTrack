import pandas as pd
import numpy as np
from typing import Union
from scipy.constants import c, physical_constants

from synapticTrack.beam import Beam, BeamWS, BeamAS
from synapticTrack.io import TrackIO, JuTrackIO, OPALIO, FlameIO, ScannerIO

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

class BeamDataIOManager:
    code_readers = {
        'track': TrackIO.read,
        'jutrack': JuTrackIO.read,
        'opal': OPALIO.read,
        'flame': FlameIO.read
    }
    code_writers = {
        'track': TrackIO.write,
        'jutrack': JuTrackIO.write,
        'opal': OPALIO.write,
        'flame': FlameIO.write
    }
    scanner_readers = {
        'wire': ScannerIO.read_wire_scanner,
        'allison': ScannerIO.read_allison_scanner
    }
    _codes = list(code_readers.keys())
    _formats = ['hdf5', 'sqlite']
    _scanners = list(scanner_readers.keys())

    @classmethod
    def read(cls, code: str, filename: str, mass_number: int, charge_state: int, 
             beam_current: float, reference_energy: float) -> Beam:
        """
        Reads beam data from a file.

        Args:
            code (str): The simulation code ('track', 'jutrack', 'opal', 'flame').
            filename (str): The name of the file to read.
            mass_number (int): Mass number of the ion species.
            charge_state (int): Charge state of the ion.
            beam_current (float): Beam current.
            reference_enegy (float): Beam reference energy in MeV/u.

        Returns:
            Beam: A Beam object containing the loaded data.
        """
        return cls.code_readers[code](filename, mass_number, charge_state, 
                                      beam_current, reference_energy)

    @classmethod
    def write(cls, code: str, filename: str, beam: Beam):
        return cls.code_writers[code](filename, beam)

    @classmethod
    def read_scanner(cls, scanner: str, filename: str) -> Union[BeamWS, BeamAS]:
        return cls.scanner_readers[scanner](filename)

    @classmethod
    def supported_codes(cls):
        return cls._codes

    @classmethod
    def supported_formats(cls):
        return cls._formats

    @classmethod
    def supported_scanners(cls):
        return cls._scanners

