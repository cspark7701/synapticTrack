import pandas as pd
from h5py import h5
import sqlite3 as sql3
from os.path import *

from synapticTrack.beam import Beam, BeamWS, BeamAS
import numpy as np
from scipy.constants import c, e, physical_constants

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

def read_track(filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    columns = ["Nseed", "iq", "dt", "dW", "x", "xp", "y", "yp"]
    df_particles = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=columns, engine='python')

    df_particles['x'] *= 10     # [cm] to [mm]
    df_particles['y'] *= 10     # [cm] to [mm]
    
    return Beam(df_particles, mass_number, charge_state, beam_current, reference_energy)

# TODO
def read_jutrack(filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    df_particles = np.zeros([6])
    return Beam(df_particles, mass_number, charge_state, beam_current, reference_energy)

# TODO
def read_opal(filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    df_particles = np.zeros([6])
    return Beam(df_particles, mass_number, charge_state, beam_current, reference_energy)

# TODO
def read_flame(filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    df_particles = np.zeros([6])
    return Beam(df_particles, mass_number, charge_state, beam_current, reference_energy)

def read_h5(filename: str) -> Beam:
    df_particles = np.zeros([6])
    return Beam(df_particles, mass_number, charge_state, beam_current, reference_energy)

def read_sqlite(filename: str) -> Beam:
    df_particles = np.zeros([6])
    return Beam(df_particles, mass_number, charge_state, beam_current, reference_energy)

def read_wire_scanner(filename: str) -> BeamWS:
    columns = ["x_pos", "x_current", "y_pos", "y_current", "d_pos", "d_current"]
    df_particles = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=columns, engine='python')

    scan_id = splitext(basename(filename))[0]

    return BeamWS(df_particles, scan_id=scan_id) 

def read_allison_scanner(filename: str) -> BeamAS:
    columns = ["x", "xp", "x_current", "hv", "y_current"]
    df_particles = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=columns, engine='python')
    
    scan_id = splitext(basename(filename))[0]

    return BeamAS(df_particles, scan_id=scan_id)

def convert_track(particle_array: np.ndarray, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    #columns = ["Nseed", "iq", "dt", "dW", "x", "xp", "y", "yp"]
    Nseed, iq, dt, dW, x, xp, y, yp = particle_array.T

    # Convert to synapticTrack units
    x_mm = x * 10
    y_mm = y * 10

    state = pd.DataFrame({
        "x": x_mm,
        "xp": xp,
        "y": y_mm,
        "yp": yp,
        "dt": dt,
        "dW": dW
    })

    return Beam(state, mass_number, charge_state, beam_current, reference_energy)

def convert_jutrack(particle_array: np.ndarray, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    #columns = ['x', 'px/p0', 'y', 'py/p0', 'z', 'delta']
    x, px_p0, y, py_p0, z, delta = particle_array.T

    # Convert JuTrack coordinates to synapticTrack
    #amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]
    E0 = mass_number * amu  # MeV
    gamma0 = 1 + reference_energy / amu
    beta0 = np.sqrt(1 - 1 / gamma0**2)
    p0 = gamma0 * beta0 * E0  # MeV/c

    # Calculate total p from delta
    p = p0 * (1 + delta)
    gamma = np.sqrt(1 + (p / E0)**2)
    dW = (gamma - gamma0) * amu  # MeV/u

    # Estimate pz/p0
    pz_p0 = np.sqrt((1 + delta)**2 - px_p0**2 - py_p0**2)

    # Convert normalized momenta to angles
    xp = (px_p0 / pz_p0) * 1e3  # mrad
    yp = (py_p0 / pz_p0) * 1e3  # mrad

    # Convert to synapticTrack units
    x_mm = x * 1e3
    y_mm = y * 1e3
    dt = -z / (beta0 * c)

    state = pd.DataFrame({
        "x": x_mm,
        "xp": xp,
        "y": y_mm,
        "yp": yp,
        "dt": dt,
        "dW": dW
    })

    return Beam(state, mass_number, charge_state, beam_current, reference_energy)

# TODO
def convert_opal(particle_array: np.ndarray, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    #columns = ["Nseed", "iq", "dt", "dW", "x", "xp", "y", "yp"]
    Nseed, iq, dt, dW, x, xp, y, yp = particle_array.T

    # Convert to synapticTrack units
    x_mm = x * 10
    y_mm = y * 10

    state = pd.DataFrame({
        "x": x_mm,
        "xp": xp,
        "y": y_mm,
        "yp": yp,
        "dt": dt,
        "dW": dW
    })

    return Beam(state, mass_number, charge_state, beam_current, reference_energy)

# TODO
def convert_flame(particle_array: np.ndarray, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
    #columns = ["Nseed", "iq", "dt", "dW", "x", "xp", "y", "yp"]
    Nseed, iq, dt, dW, x, xp, y, yp = particle_array.T

    # Convert to synapticTrack units
    x_mm = x * 10
    y_mm = y * 10

    state = pd.DataFrame({
        "x": x_mm,
        "xp": xp,
        "y": y_mm,
        "yp": yp,
        "dt": dt,
        "dW": dW
    })

    return Beam(state, mass_number, charge_state, beam_current, reference_energy)

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

    #amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]
    
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

class BeamDataIO:
    _codes = ['track', 'jutrack', 'opal', 'flame']
    _formats = ['hdf5', 'sqlite']
    _scanners = ['wire', 'allison']

    def __init__(self):
        self._code_readers = {'track': read_track, 'jutrack': read_jutrack, 'opal': read_opal, 'flame': read_flame}
        self._code_writers = {'track': self.write_track, 'jutrack': self.write_jutrack, 'opal': self.write_opal, 'flame': self.write_flame}
        self._code_converters = {'track': convert_track, 'jutrack': convert_jutrack, 'opal': convert_opal, 'flame': convert_track}
        self._file_readers = {'hdf5': read_h5, 'sqlite': read_sqlite}
        self._file_writers = {'hdf5': self.write_h5, 'sqlite': self.write_sqlite}

        self._scanner_readers = {'wire': read_wire_scanner, 'allison': read_allison_scanner}
        #self._scanner_writers = {'wire': self.write_wire_scanner, 'allison': write_allison_scanner}

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

    def read(self, code: str, filename: str, mass_number: int, charge_state: int, beam_current: float, reference_energy: float) -> Beam:
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
        reader = self._code_readers[code]
        beam = reader(filename, mass_number, charge_state, beam_current, reference_energy)
        return beam

    def read_scanner(self, scanner: str, filename: str) -> BeamWS:
        """
        Reads beam scanner data from a file.

        Args:
            scanner (str): scanner type ('wire', 'allison')
            filename (str): The name of the file to read.

        Returns:
            BeamWS: A Beam Wire Scanner object containing the loaded data.
        """
        reader = self._scanner_readers[scanner]
        beam_diag_data = reader(filename)
        return beam_diag_data

    def convert(self, code: str, particle_array: np.ndarray, mass_number: int, charge_state: int, beam_current: float, reference_energy:float) -> Beam:
        converter = self._code_converters[code]
        return converter(particle_array, mass_number, charge_state, beam_current, reference_energy)

    # TODO
    def write_track(self, filename: str, beam: Beam):
        """Writes beam data to a TRACK file.  (Example -  Implement this)"""
        print(f"Writing to TRACK file: {filename}")
        print(beam.state.head())  # Example
        pass  # Replace with actual implementation

    def write_jutrack(self, filename: str, beam: Beam):
        """
        Save the JuTrack-compatible r matrix to a plain text file.

        Args:
            filename (str): Path to save the r matrix (.dat or .txt).
            beam (Beam): synapticTrack beam object.
        """
        print(f"Writing to JuTrack file: {filename}")
        jutrack_df = convert_to_jutrack_coordinates(beam)
        jutrack_df.to_csv(filename, sep=' ', header=False, index=False, float_format='%.12e')
        pass 

    # TODO
    def write_opal(self, filename: str, beam: Beam):
        """Writes beam data to an OPAL file. (Example - Implement this)"""
        print(f"Writing to OPAL file: {filename}")
        print(beam.state.head())
        pass

    # TODO
    def write_flame(self, filename: str, beam: Beam):
        """Writes beam data to a FLAME file. (Example - Implement this)"""
        print(f"Writing to FLAME file: {filename}")
        print(beam.state.head())
        pass

    # TODO
    def write_h5(self, filename: str, beam: Beam):
        """Writes beam data to an HDF5 file. (Example - Implement this)"""
        print(f"Writing to HDF5 file: {filename}")
        beam.state.to_hdf(filename, key='beam_data', mode='w')
        pass

    # TODO
    def write_sqlite(self, filename: str, beam: Beam):
        """Writes beam data to a SQLite file. (Example - implement this)"""
        print(f"Writing to SQLite file: {filename}")
        beam.state.to_sql('beam_data', f'sqlite:///{filename}', if_exists='replace')
        pass
