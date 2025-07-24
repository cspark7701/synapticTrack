import pytest
import numpy as np
import pandas as pd
from synapticTrack.beam import Beam, BeamWS, BeamAS

@pytest.fixture
def example_beam_data():
    rng = np.random.default_rng(seed=42)
    return rng.normal(loc=0.0, scale=1.0, size=(10000, 6))  # x, xp, y, yp, dt, dW

@pytest.fixture
def example_beam(example_beam_data):
    df = pd.DataFrame(example_beam_data, columns=['x', 'xp', 'y', 'yp', 'dt', 'dW'])
    return Beam(df, mass_number=12, charge_state=6, beam_current=1.0, reference_energy=0.01)

@pytest.fixture
def example_beamws():
    rng = np.random.default_rng(seed=123)
    x_pos = np.linspace(-5, 5, 100)
    y_pos = np.linspace(-5, 5, 100)
    x_current = np.exp(-x_pos**2 / 2)
    y_current = np.exp(-y_pos**2 / 2)
    data = pd.DataFrame({
        'x_pos': x_pos,
        'x_current': x_current,
        'y_pos': y_pos,
        'y_current': y_current,
        'd_pos': np.zeros_like(x_pos),
        'd_current': np.zeros_like(x_pos)
    })
    return BeamWS(data, scan_id='WS01')

@pytest.fixture
def example_beamas():
    rng = np.random.default_rng(seed=321)
    x = np.linspace(-5, 5, 100)
    xp = np.linspace(-50, 50, 100)
    x_current = np.exp(-x**2 / 2)
    data = pd.DataFrame({
        'x': x,
        'xp': xp,
        'x_current': x_current,
        'hv': np.zeros_like(x),
        'y_current': np.zeros_like(x)
    })
    return BeamAS(data, scan_id='AS01')

