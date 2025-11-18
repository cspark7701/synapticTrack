import pytest
from synapticTrack.lattice.track_lattice import Lattice

def test_lattice_parse_exists():
    assert hasattr(Lattice, "parse"), "Lattice.parse should be implemented"

def test_lattice_parse_raises_on_malformed_line(tmp_path):
    lattice_file = tmp_path / "lattice.lat"
    lattice_file.write_text("MALFORMED_LINE\n")
    parse_func = getattr(Lattice, "parse")

    # call parse in a way that handles both classmethod/staticmethod and instance method forms
    with pytest.raises((ValueError, IndexError, TypeError, FileNotFoundError)):
        try:
            # try calling as a callable that accepts a filename
            parse_func(str(lattice_file))
        except TypeError:
            # fallback: instantiate and call parse as instance method
            Lattice().parse(str(lattice_file))
