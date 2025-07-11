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
    assert "x_center" in results
    assert "y_center" in results
    assert "sigma_x" in results
    assert "sigma_y" in results
    assert "gaussian_sigma_x_fit" in results
    assert "gaussian_sigma_y_fit" in results

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
    assert "x_center" in results
    assert "xp_center" in results
    assert "sigma_x" in results
    assert "sigma_xp" in results
    assert "gaussian_sigma_x_fit" in results
    assert "gaussian_sigma_xp_fit" in results
    assert "geometric_emittance" in results

