import json
import pytest
from synapticTrack.io.beam_data_io_manager import BeamDataIOManager

def _simple_reader(filename, mass_number, charge_state, beam_current, reference_energy):
    # return a tuple so tests can assert values directly
    return (filename, mass_number, charge_state, beam_current, reference_energy)

def test_read_without_json(tmp_path, monkeypatch):
    data_file = tmp_path / "beam.dat"
    data_file.write_text("dummy data")
    # register a simple reader for test code
    BeamDataIOManager.code_readers = {"testcode": _simple_reader}
    res = BeamDataIOManager.read("testcode", str(data_file),
                                 mass_number=1, charge_state=2,
                                 beam_current=0.5, reference_energy=3.0)
    assert res == (str(data_file), 1, 2, 0.5, 3.0)

def test_read_with_json_overrides(tmp_path):
    data_file = tmp_path / "beam.dat"
    data_file.write_text("dummy data")
    json_file = tmp_path / "beam.json"
    metadata = {"mass_number": "7", "beam_current": 1.23}
    json_file.write_text(json.dumps(metadata))
    BeamDataIOManager.code_readers = {"testcode": _simple_reader}
    res = BeamDataIOManager.read("testcode", str(data_file),
                                 mass_number=1, charge_state=2,
                                 beam_current=0.5, reference_energy=3.0)
    # mass_number overridden -> int(7), beam_current overridden -> float(1.23)
    assert res == (str(data_file), 7, 2, 1.23, 3.0)

def test_read_with_bad_types_in_json_raises(tmp_path):
    data_file = tmp_path / "beam.dat"
    data_file.write_text("dummy data")
    json_file = tmp_path / "beam.json"
    # invalid mass_number that cannot be converted to int
    metadata = {"mass_number": "not-an-int"}
    json_file.write_text(json.dumps(metadata))
    BeamDataIOManager.code_readers = {"testcode": _simple_reader}
    with pytest.raises(ValueError):
        BeamDataIOManager.read("testcode", str(data_file))
