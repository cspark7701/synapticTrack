from synapticTrack import beam

def test_import_io():
    assert beam is not None

# TODO
#def test_beam_validation():
#    base_dir = '../data/input_beam'
#    filename = base_dir + '/' + 'coord.out'

#    beam_io = BeamDataIO() 
#    synpatic_beam = beam_io.read(code='track', filename=filename, mass_number=40, charge_state=8, beam_current=0, reference_energy=0.010)

#    assert_frame_equal(convert_to_jutrack_coordinates(convert_jutrack(particles, ...)), original_data)

