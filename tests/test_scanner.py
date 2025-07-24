# tests/test_scanner.py
import pytest
import os
import warnings
from pathlib import Path
from synapticTrack.io import BeamDataIOManager
from synapticTrack.analysis import analyze_wire_scanner, analyze_allison_scanner_2d

@pytest.fixture
def wire_scanner_dir():
    return Path(__file__).parent / "data" / "scanner" / "2_exp_LEBT_WS"

@pytest.mark.parametrize("wire_scanner_filename", [
    "ECR32-WS001-100717.txt",
    "LEBT-WS002-100523.txt",
    "LEBT-WS003-100325.txt",
    "LEBT-WS004-100044.txt"
])

def test_wire_scanner_analysis(wire_scanner_dir, wire_scanner_filename):
    filepath = os.path.join(wire_scanner_dir, wire_scanner_filename)
    beam = BeamDataIOManager.read_scanner(scanner="wire", filename=filepath)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        results = analyze_wire_scanner(beam, plot=False)

    assert "x_center" in results
    assert "y_center" in results
    assert "sigma_x" in results
    assert "sigma_y" in results
    assert "gaussian_sigma_x_fit" in results
    assert "gaussian_sigma_y_fit" in results

@pytest.fixture
def allison_scanner_dir():
    return Path(__file__).parent / "data" / "scanner" / "3_exp_Allison"

@pytest.mark.parametrize("allison_scanner_filename", [
    "101614_X.txt",
    "102829_Y.txt"
])

def test_allison_scanner_analysis(allison_scanner_dir, allison_scanner_filename):
    filepath = os.path.join(allison_scanner_dir, allison_scanner_filename)
    beam = BeamDataIOManager.read_scanner(scanner="allison", filename=filepath)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        results = analyze_allison_scanner_2d(beam, plot=False)

    assert "x_center" in results
    assert "xp_center" in results
    assert "sigma_x" in results
    assert "sigma_xp" in results
    assert "gaussian_sigma_x_fit" in results
    assert "gaussian_sigma_xp_fit" in results
    assert "covariance_x_xp" in results
    assert "emittance_rms" in results
    assert "emittance_geometric" in results

