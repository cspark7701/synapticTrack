#tests/test_beam.py
import pytest
from synapticTrack.beam import Twiss
from synapticTrack.io import BeamDataIOManager
from pathlib import Path

TEST_DIR = Path(__file__).parent
DATA_DIR = TEST_DIR / "data" / "input_beam"

@pytest.fixture
def example_beam():
    """Fixture for loading example beam using BeamDataIOManager from TRACK file."""
    filename = DATA_DIR / "coord.out"
    assert filename.exists(), f"Test input file not found: {filename}"
    return BeamDataIOManager.read(
        code='track',
        filename=filename,
        mass_number=40,
        charge_state=8,
        beam_current=0.0,
        reference_energy=0.010  # MeV/u
    )

def test_beam_loading(example_beam):
    """Test basic integrity of loaded beam object."""
    assert example_beam.state is not None, "Beam state should not be None"
    assert not example_beam.state.empty, "Beam state should not be empty"
    for col in ['x', 'xp', 'y', 'yp', 'dt', 'dW']:
        assert col in example_beam.state.columns, f"Missing column: {col}"

def test_twiss_computation(example_beam):
    """Test that Twiss parameters are computed for all planes."""
    twiss = Twiss(example_beam)
    for name, plane in zip(['horizontal', 'vertical', 'longitudinal'],
                           [twiss.horizontal, twiss.vertical, twiss.longitudinal]):
        assert isinstance(plane, dict), f"{name} Twiss parameters must be a dict"
        for key in ['alpha', 'beta', 'emittance']:
            assert key in plane, f"Missing '{key}' in {name} Twiss"
        assert plane['beta'] > 0, f"{name} β must be > 0"
        assert plane['emittance'] > 0, f"{name} ε must be > 0"

def test_normalized_emittance(example_beam):
    """Test normalized emittance calculation returns valid results."""
    twiss = Twiss(example_beam)
    for plane in ['x', 'y', 'z']:
        norm_emit = twiss.normalized_emittance(plane)
        assert isinstance(norm_emit, float), f"Emittance for {plane} should be float"
        assert norm_emit > 0, f"Emittance for {plane} should be > 0"

def test_all_normalized_emittances(example_beam):
    """Test dictionary output of normalized emittances."""
    twiss = Twiss(example_beam)
    norm_emits = twiss.normalized_emittances()
    assert isinstance(norm_emits, dict), "Normalized emittances should return a dict"
    for plane in ['x', 'y', 'z']:
        assert plane in norm_emits, f"{plane} missing in normalized emittances"
        assert isinstance(norm_emits[plane], float)
        assert norm_emits[plane] > 0

