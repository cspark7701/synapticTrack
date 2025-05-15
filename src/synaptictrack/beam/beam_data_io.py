import pandas as pd
from h5py import h5
import sqlite3 as sql3
from os.path import *
from synaptictrack.beam import Beam, BeamWS, BeamAS
from synaptictrack.beam import BeamWS

def read_track(filename: str, mass_number: int, charge_state: int, beam_current: float) -> Beam:
    columns = ["Nseed", "iq", "dt", "dW", "x", "xp", "y", "yp"]
    df_particles = pd.read_csv(filename, sep='\s+', skiprows=1, names=columns, engine='python')

    df_particles['x'] *= 10     # [cm] to [mm]
    df_particles['y'] *= 10     # [cm] to [mm]
    
    beam = Beam(df_particles, mass_number, charge_state, beam_current)
    return beam

def read_opal(filename: str, mass_number: int, charge_state: int, beam_current: float) -> Beam:
    df_particles = np.zeros([6])
    Beam(df_particles, mass_number, charge_state, beam_current)
    return beam

def read_flame(filename: str, mass_number: int, charge_state: int, beam_current: float) -> Beam:
    df_particles = np.zeros([6])
    Beam(df_particles, mass_number, charge_state, beam_current)
    return beam

def read_h5(filename: str) -> Beam:
    df_particles = np.zeros([6])
    Beam(df_particles, mass_number, charge_state, beam_current)
    return beam

def read_sqlite(filename: str) -> Beam:
    df_particles = np.zeros([6])
    Beam(df_particles, mass_number, charge_state, beam_current)
    return beam

def read_wire_scanner(filename: str) -> BeamWS:
    columns = ["x_pos", "x_current", "y_pos", "y_current", "d_pos", "d_current"]
    df_particles = pd.read_csv(filename, sep='\s+', skiprows=1, names=columns, engine='python')

    scan_id = splitext(basename(filename))[0]

    beam_ws = BeamWS(df_particles, scan_id=scan_id) 

    return beam_ws

def read_alison_scanner(filename: str) -> BeamAS:
    columns = ["x_position", "x_angle", "x_current", "hv", "y_current"]
    df_particles = pd.read_csv(filename, sep='\s+', skiprows=1, names=columns, engine='python')
    
    scan_id = splitext(basename(filename))[0]

    beam_as = BeamAS(df_particles, scan_id=scan_id)

    return beam_as

class BeamDataIO:
    _codes = ['track', 'opal', 'flame']
    _formats = ['hdf5', 'sqlite']
    _scanners = ['wire', 'alison']

    def __init__(self):
        self._code_readers = {'track': read_track, 'opal': read_opal, 'flame': read_flame}
        self._code_writers = {'track': self.write_track, 'opal': self.write_opal, 'flame': self.write_flame
}
        self._file_readers = {'hdf5': read_h5, 'sqlite': read_sqlite}
        self._file_writers = {'hdf5': self.write_h5, 'sqlite': self.write_sqlite}

        self._scanner_readers = {'wire': read_wire_scanner, 'alison': read_alison_scanner}
        #self._scanner_writers = {'wire': self.write_wire_scanner, 'alison': write_alison_scanner}

    def check_supported_codes(self, code):
        if code in self.supported_codes():
            return True
        else:
            return False

    @classmethod
    def supported_codes(cls):
        return cls._codes

    @classmethod
    def supported_formats(cls):
        return cls._formats

    @classmethod
    def supported_scanners(cls):
        return cls._scanners

    def read(self, code: str, filename: str, mass_number: int, charge_state: int, beam_current: float) -> Beam:
        """
        Reads beam data from a file.

        Args:
            code (str): The simulation code ('track', 'opal', 'flame').
            filename (str): The name of the file to read.
            mass_number (int): Mass number of the ion species.
            charge_state (int): Charge state of the ion.
            beam_current (float): Beam current.

        Returns:
            Beam: A Beam object containing the loaded data.
        """
        reader = self._code_readers[code]
        beam = reader(filename, mass_number, charge_state, beam_current)
        return beam

    def read_scanner(self, scanner: str, filename: str) -> BeamWS:
        """
        Reads beam scanner data from a file.

        Args:
            scanner (str): scanner type ('wire', 'alison')
            filename (str): The name of the file to read.

        Returns:
            BeamWS: A Beam Wire Scanner object containing the loaded data.
        """
        reader = self._scanner_readers[scanner]
        beam_diag_data = reader(filename)
        return beam_diag_data

    def write_track(self, filename: str, beam: Beam):
        """Writes beam data to a TRACK file.  (Example -  Implement this)"""
        print(f"Writing to TRACK file: {filename}")
        print(beam.state.head())  # Example
        pass  # Replace with actual implementation

    def write_opal(self, filename: str, beam: Beam):
        """Writes beam data to an OPAL file. (Example - Implement this)"""
        print(f"Writing to OPAL file: {filename}")
        print(beam.state.head())
        pass

    def write_flame(self, filename: str, beam: Beam):
        """Writes beam data to a FLAME file. (Example - Implement this)"""
        print(f"Writing to FLAME file: {filename}")
        print(beam.state.head())
        pass

    def write_h5(self, filename: str, beam: Beam):
        """Writes beam data to an HDF5 file. (Example - Implement this)"""
        print(f"Writing to HDF5 file: {filename}")
        beam.state.to_hdf(filename, key='beam_data', mode='w')
        pass

    def write_sqlite(self, filename: str, beam: Beam):
        """Writes beam data to a SQLite file. (Example - implement this)"""
        print(f"Writing to SQLite file: {filename}")
        beam.state.to_sql('beam_data', f'sqlite:///{filename}', if_exists='replace')
        pass
