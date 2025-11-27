import os
import numpy as np
import pandas as pd

from synapticTrack.io import BeamDataIOManager
from synapticTrack.lattice.track_elements import *
from synapticTrack.lattice.track_lattice import Lattice
from synapticTrack.track.run_track import *

def load_LEBT_lattice():
    elements_list = []
    stms = []
    equads = []
    for i in range(0, 6):
        fname = f'lattice/elements{i}.json'
        elements = Lattice.from_json(fname)
        elements_list.append(elements)
        for elem in elements:
            name = elem.get_name()
            if "stm" in name:
                stms.append(elem)
            elif "eq" in name:
                equads.append(elem)
    return (elements_list, stms, equads)



def set_stm_strengths(stms, fhkick, fvkick):
    """
    Set steering magnet strengths
    stms: list
        list of steering magnets
    fhkick: list
        list of horizontal kick strengths [mrad]
    fvkick: list
        list of vertical kick strengths [mrad]
    """
    for i, stm in enumerate(stms):
        stms[i].FHkick = fhkick[i]
        stms[i].FVkick = fvkick[i]


def set_equad_strengths(equads, Vfs):
    """
    Set equads strengths
    equads: list
        list of equads
    Vfs: np array
        new equad strengths in voltages
    """
    for i, equad in enumerate(equads):
        equad.Vf = Vfs[i]


def get_z_scanner(output_dir):
    z_scanner = []
    with open(os.path.join(output_dir, 'z_scanner.out'), 'r') as f:
        for line in f:
            z_scanner.append(line.strip())
    return (z_scanner)

def create_z_scanner(elements_list, output_dir_list, final_output_dir):
    z_scanner = []
    lattice_length = 0
    for elements, output_dir in zip(elements_list, output_dir_list):
        sclinac = Lattice(elements)
        #print('\n')
        for elem in sclinac:
            elem_name = elem.get_name()
            elem_length = elem.get_length()
            lattice_length += elem_length
            #print (f"{elem_name}, {elem_length:3.6f}, {lattice_length*0.01:6.6f}")
        z_scanner.append(lattice_length)

    with open(os.path.join(final_output_dir, 'z_scanner.out'), 'w') as f:
        for item in z_scanner:
            f.write(str(item) + '\n')

def get_rms_beam_size(output_dir, exclude_allison=1, verbose=0):

    z_scanner = get_z_scanner(output_dir)
    if exclude_allison:
        z_scanner.pop(1)

    coord_list = ['coord_wire_scanner1.out', 'coord_wire_scanner2.out', 'coord_wire_scanner3.out', 'coord_wire_scanner4.out']

    sim_rms_size = pd.DataFrame(columns=['z', 'x', 'xp', 'y', 'yp', 'dt', 'dW'])
    sim_rms_x = np.zeros(4, dtype=float)
    sim_rms_y = np.zeros(4, dtype=float)

    for i, file in enumerate(coord_list):
        filename = os.path.join(output_dir, file)

        beam_io_manager = BeamDataIOManager()
        beam = beam_io_manager.read(code='track', filename=filename, mass_number=40, charge_state=8, beam_current=0, reference_energy=0.10)

        sim_rms_size.loc[len(sim_rms_size)] = beam.rms_size
        sim_rms_size.loc[i, 'z'] = float(z_scanner[i])*10

        sim_rms_x[i] = sim_rms_size.loc[i, 'x']
        sim_rms_y[i] = sim_rms_size.loc[i, 'y']

        if verbose == 1:
            print('simulation rms size')
            print(sim_rms_size)

    return (sim_rms_x, sim_rms_y)


def get_beam_data(output_dir, output_files):
    """
    Get beam centroid data
    output_dir: str
        diretory for beam data
    output_files: list
        list of output files
    """
    z_scanner = [198.12185300000002, 400.821853, 764.0236130000001, 998.7236130000001, 1076.7236130000001, 1228.323613]

    beam_centroid = pd.DataFrame(columns=['z', 'x', 'xp', 'y', 'yp', 'dt', 'dW'])
    beam_rms_size = pd.DataFrame(columns=['z', 'x', 'xp', 'y', 'yp', 'dt', 'dW'])
    for i, file in enumerate(output_files):
        filename = os.path.join(output_dir, file)

        beam_io_manager = BeamDataIOManager() 
        beam = beam_io_manager.read(code='track', filename=filename, mass_number=40, charge_state=8, beam_current=0, reference_energy=0.10)
        beam_centroid.loc[len(beam_centroid)] = beam.centroid
        beam_rms_size.loc[len(beam_rms_size)] = beam.rms_size
        beam_centroid.loc[i, 'z'] = z_scanner[i]*10
        beam_rms_size.loc[i, 'z'] = z_scanner[i]*10

    return (beam_centroid, beam_rms_size)


def copy_step_output_files(final_output_dir, output_dir_list, final_output_files):
    """
    Copy step output files to final output directory
    final_output_dir: str
        destination directory
    output_dir_list: list
        list of output directories
    final_output_files:
        list of output files
    """
    for output_dir, final_output_file in zip(output_dir_list, final_output_files):
        #print(output_dir, os.path.join(final_output_dir, final_output_file))
        shutil.copy(os.path.join(output_dir, "coord.out"), os.path.join(final_output_dir, final_output_file))


def copy_track_output_files(final_output_dir, output_dir_list):
    """
    Copy track output files to final output directory
    final_output_dir: str
        destination directory
    output_dir_list: list
        list ot output directories
    """
    output_files = ["beam.out", "step.out", "lost.out"]
    z_offset_beam = 0.0
    step_offset = 0.0
    
    for output_file in output_files:
        output_path = os.path.join(final_output_dir, output_file)

        with open(output_path, 'w') as outfile:
            for i, output_dir in enumerate(output_dir_list):
                file_path = os.path.join(output_dir, output_file)
                if not os.path.isfile(file_path):
                    print(f"Warning: {file_path} does not exist. Skipping.")
                    continue

                with open(file_path, 'r') as infile:
                    lines = infile.readlines()

                    # 1. Handle beam.out: adjust 3rd column
                    if output_file == "beam.out":
                        lines = lines[:-1]  # Remove last line
                        header = lines[:3] if i == 0 else []
                        data = lines[3:]

                        if not data:
                            continue

                        adjusted_data = []
                        for line in data:
                            parts = line.strip().split()
                            if len(parts) < 3:
                                continue
                            try:
                                z_val = float(parts[2]) + z_offset_beam
                                parts[2] = f"{z_val:.6f}"
                                adjusted_data.append(" ".join(parts) + "\n")
                            except ValueError:
                                continue

                        # Update offset using last z
                        try:
                            last_z = float(adjusted_data[-1].split()[2])
                            z_offset_beam = last_z
                        except IndexError:
                            pass

                        if header:
                            outfile.writelines(header)
                        sep_filename = f"beam{i}.out"
                        with open(os.path.join(final_output_dir, sep_filename), 'w') as sep_file:
                            sep_file.writelines(adjusted_data)
                        outfile.writelines(adjusted_data)

                    # 2. Handle step.out: adjust 1st column
                    elif output_file == "step.out":
                        header = lines[:4] if i == 0 else []
                        data = lines[4:]

                        if not data:
                            continue

                        adjusted_data = []
                        for line in data:
                            parts = line.strip().split()
                            if len(parts) < 1:
                                continue
                            try:
                                s_val = float(parts[0]) + step_offset
                                parts[0] = f"{s_val:.6f}"
                                adjusted_data.append(" ".join(parts) + "\n")
                            except ValueError:
                                continue

                        # Update offset using last s
                        try:
                            last_s = float(adjusted_data[-1].split()[0])
                            step_offset = last_s
                        except IndexError:
                            pass
    
                        if header:
                            outfile.writelines(header)
                        outfile.writelines(adjusted_data)
    
                    # 3. Handle lost.out: just merge, skip 1-line header
                    elif output_file == "lost.out":
                        if i == 0:
                            outfile.writelines(lines)
                        elif len(lines) > 1:
                            outfile.writelines(lines[1:])


def run_track_steps(elements_list, output_dir_list):
    """
    Run track simulations for each lattice segments
    elements_list: list
        list of lattice segments
    output_dir_list: list
        list of output directoies for each lattice segment
    """
    load_beam = 2
    for elements, output_dir in zip(elements_list, output_dir_list):
        #print ("\nRunning", output_dir)
        sclinac = Lattice(elements)
        sclinac.write(load_beam=load_beam)

        # runt TRACK simulations for given lattice segment
        run_track(output_dir=output_dir, verbose=0)
        load_beam += 1



