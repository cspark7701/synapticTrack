import pandas as pd
import numpy as np
from os.path import splitext, exists
import json
from typing import Union
from scipy.constants import c, physical_constants

from synapticTrack.beam import *
from synapticTrack.io import *

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
    def read(cls, code: str, filename: str,
             mass_number: int = None, charge_state: int = None,
             beam_current: float = None, reference_energy: float = None) -> Beam:
        """
        Reads beam data from a file. If a metadata .json file exists,
        it overrides the passed parameters.

        Args:
            code (str): Simulation code ('track', 'jutrack', 'opal', 'flame')
            filename (str): Path to the beam particle file
            mass_number (int, optional): Mass number of the ion
            charge_state (int, optional): Charge state
            beam_current (float, optional): Beam current
            reference_energy (float, optional): Reference energy in MeV/u

        Returns:
            Beam: A Beam object with data and metadata
        """

        json_path = splitext(filename)[0] + ".json"

        if exists(json_path):
            try:
                # read_beam_metadata should accept a filename/path to the json
                metadata = cls.read_beam_metadata(json_path)
            except Exception as e:
                raise ValueError(f"Failed to read metadata from '{json_path}': {e}") from e

            def _to_int(val, name):
                if val is None:
                    return None
                try:
                    return int(val)
                except Exception:
                    raise ValueError(f"Invalid integer for '{name}': {val}")

            def _to_float(val, name):
                if val is None:
                    return None
                try:
                    return float(val)
                except Exception:
                    raise ValueError(f"Invalid float for '{name}': {val}")

            # Use metadata values if present, otherwise keep passed-in values
            mass_number = _to_int(metadata.get("mass_number", mass_number), "mass_number")
            charge_state = _to_int(metadata.get("charge_state", charge_state), "charge_state")
            beam_current = _to_float(metadata.get("beam_current", beam_current), "beam_current")
            reference_energy = _to_float(metadata.get("reference_energy", reference_energy), "reference_energy")

        if code not in cls.code_readers:
            raise KeyError(f"No reader registered for code '{code}'")

        return cls.code_readers[code](filename, mass_number, charge_state, beam_current, reference_energy)

    @classmethod
    def write(cls, code: str, filename: str, beam: Beam):
        # 1. Save beam particle coordinates
        cls.code_writers[code](filename, beam)

        # 2. Create metadata dictionary
        def to_serializable(d):
            """Convert all values to serializable (e.g., float) format."""
            return {k: float(v) for k, v in d.items()}

        twiss = Twiss(beam)
        metadata = {
            "species": beam.species,
            "charge_state": beam.charge_state,
            "mass_number": beam.mass_number,
            "beam_current": beam.beam_current,
            "reference_energy": beam.reference_energy,
            "macroparticles": beam.macroparticles,
            "beam_centroid": to_serializable(beam.centroid),
            "beam_sigma": to_serializable(beam.rms_size),
            "twiss_x": to_serializable(twiss.horizontal),
            "twiss_y": to_serializable(twiss.vertical),
            "twiss_z": to_serializable(twiss.longitudinal)
        }
        # 3. Determine JSON filename
        json_filename = splitext(filename)[0] + ".json"

        # 4. Write JSON metadata
        with open(json_filename, "w") as f:
            json.dump(metadata, f, indent=4)

    @classmethod
    def read_beam_metadata(cls, filename: str) -> dict:
        """
        Reads the beam metadata (charge_state, mass_number, etc.) from a corresponding .json file.

        Args:
            filename (str): Path to the code-specific particle coordinate file.

        Returns:
            dict: Dictionary with metadata keys and values.
        """
        json_filename = splitext(filename)[0] + ".json"
        with open(json_filename, "r") as f:
            metadata = json.load(f)
        print(json.dumps(metadata, indent=4))
        return metadata

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

