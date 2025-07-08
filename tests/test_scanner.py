# tests/test_scanner.py
import numpy as np
import pandas as pd
from synapticTrack.beam.beam_scanner import BeamWS, BeamAS
from synapticTrack.analysis.scanner_analysis import analyze_wire_scanner, analyze_allison_scanner_2d

def test_analyze_wire_scanner():
    # Simulated data
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-4, 4, 100)
    x_current = np.exp(-x**2 / 2)
    y_current = np.exp(-y**2 / 2)
    df = pd.DataFrame({
        'x_pos': x,
        'x_current': x_current,
        'y_pos': y,
        'y_current': y_current,
        'd_pos': np.zeros_like(x),
        'd_current': np.zeros_like(x),
    })
    beam = BeamWS(df, scan_id="test_ws")
    results = analyze_wire_scanner(beam, plot=False)
    assert "sigma_x_mm" in results
    assert "sigma_y_mm" in results
    assert results["sigma_x_mm"] > 0


def test_analyze_allison_scanner_2d():
    x = np.random.normal(0, 1, 1000)
    xp = np.random.normal(0, 0.5, 1000)
    x_current = np.exp(-(x**2 + xp**2))
    df = pd.DataFrame({
        'x': x,
        'xp': xp,
        'x_current': x_current,
    })
    beam = BeamAS(df, scan_id="test_as2d")
    results = analyze_allison_scanner_2d(beam, plot=False)
    assert "geometric_emittance_mm_mrad" in results
    assert results["geometric_emittance_mm_mrad"] > 0

