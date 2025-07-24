import os
import numpy as np
import pytest
import pandas as pd
from pathlib import Path
from julia import Main
from scipy.constants import c, physical_constants
from synapticTrack.beam import Beam
from synapticTrack.io import BeamDataIOManager, JuTrackIO

amu = physical_constants['atomic mass constant energy equivalent in MeV'][0]

@pytest.fixture(scope="module")
def activate_jutrack():
    """Activate external JuTrack.jl environment using PyJulia."""
    jutrack_path = os.getenv("JuTrack_Path", "/tmp/JuTrack.jl")
    assert os.path.exists(jutrack_path), f"JuTrack path not found: {jutrack_path}"

    Main.eval(f'using Pkg; Pkg.activate("{jutrack_path}"); Pkg.instantiate()')
    Main.eval("using JuTrack")
    Main.eval("using DelimitedFiles")

@pytest.fixture
def track_beam():
    filepath = Path(__file__).parent / "data" / "input_beam" / "coord.out"
    assert filepath.exists(), f"Missing beam file: {filepath}"
    return BeamDataIOManager.read(
        'track',
        filename=str(filepath),
        mass_number=40,
        charge_state=8,
        beam_current=0.0,
        reference_energy=0.010
    )

def test_jutrack_beam(activate_jutrack, track_beam, tmp_path):
    """Tracks beam using JuTrack.jl via PyJulia."""
    # Write beam to JuTrack format
    beam_file = tmp_path / "jubeam_input.dat"
    BeamDataIOManager.write('jutrack', filename=str(beam_file), beam=track_beam)

    # Load and track in Julia
    #Main.include("JuTrack.jl")  # optional if you want to include a script
    Main.input_file = str(beam_file)
    Main.output_file = str(tmp_path / "jubeam_output.dat")

    Main.mass_number = track_beam.mass_number
    Main.charge = float(track_beam.charge_state)
    Main.current = track_beam.beam_current
    Main.rest_mass = track_beam.mass_number * amu * 1e6
    Main.energy = track_beam.reference_energy + Main.rest_mass

    Main.eval("""
        particles = readdlm(input_file)
        beam = Beam(particles, energy=energy, charge=charge, mass=rest_mass, current=current)
    """)

    # convet back the JuTrack Beam
    jubeam = Main.beam
    jutrack_beam = JuTrackIO.convert(
        jubeam.r,
        mass_number=Main.mass_number,
        charge_state=int(jubeam.charge),
        beam_current=jubeam.current,
        reference_energy=(jubeam.energy - jubeam.mass)*1e6
    )

    assert isinstance(jutrack_beam, Beam)
    assert not jutrack_beam.state.empty
    assert 'x' in jutrack_beam.state.columns
    assert 'xp' in jutrack_beam.state.columns
    assert jutrack_beam.state.shape == track_beam.state.shape - 2


