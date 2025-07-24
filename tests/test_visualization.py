#tests/test_visualization.py

import pytest
import tempfile
import os
from pathlib import Path
from synapticTrack.io import BeamDataIOManager
from synapticTrack.visualizations.plot_phasespace import phasespace_plot

TEST_DIR = Path(__file__).parent
DATA_DIR = TEST_DIR / "data" / "input_beam"

@pytest.fixture
def example_beam():
    filename = DATA_DIR / "coord.out"
    assert filename.exists(), f"Missing test beam file: {filename}"
    return BeamDataIOManager.read(
        code='track',
        filename=filename,
        mass_number=40,
        charge_state=8,
        beam_current=0.0,
        reference_energy=0.10
    )

def test_phasespace_plot_xy(example_beam):
    x = example_beam.x
    xp = example_beam.xp
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "phasespace_xy.png")
        phasespace_plot(
            x, xp,
            x_center=example_beam.centroid["x"],
            y_center=example_beam.centroid["xp"],
            xyrange=[-20, 20, -20, 20],
            title="Horizontal Phase Space",
            xlabel=r"$x$ [mm]",
            ylabel=r"$x'$ [mrad]",
            nbins=100,
            projection=0,
            density=True,
            cmap="viridis",
            figname=output_path
        )
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

