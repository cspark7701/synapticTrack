import os
import shutil
import subprocess
import platform

output_list = ["sclinac.dat", "lost.out", "linac.dat", "ini_dis.dat", "step.out", "refp.out",
               "beam.out", "coord.out", "read_dis.out", "log.out", "sc_warn.out"]

def run_track(track_exe_path="TRACKv39C.exe", input_dir=".", output_dir=None, verbose=False):
    """
    Run TRACK simulation using TRACKv39C.exe.
    
    On Linux: runs with 'wine'
    On Windows: runs directly
    """
    track_dat_path = os.path.join(input_dir, "track.dat")
    if not os.path.isfile(track_dat_path):
        raise FileNotFoundError(f"{track_dat_path} is missing.")

    track_lat_path = os.path.join(input_dir, "sclinac.dat")
    if not os.path.isfile(track_lat_path):
        raise FileNotFoundError(f"{track_lat_path} is missing.")

    track_beam_path = os.path.join(input_dir, "scratch.#02")
    if not os.path.isfile(track_beam_path):
        raise FileNotFoundError(f"{track_beam_path} is missing.")

    extra_files = ["fi_in.dat"]
    for f in extra_files:
        track_extra_path = os.path.join(input_dir, f)
        if not os.path.isfile(track_extra_path):
            raise FileNotFoundError(f"{track_extra_path} is missing.")

    system = platform.system()
    if verbose:
        print(f"Detected OS: {system}")
        print(f"Running TRACK in directory: {os.path.abspath(input_dir)}")

    if system == "Linux":
        cmd = ["wine", track_exe_path]
    elif system == "Windows":
        cmd = [track_exe_path]
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    try:
        if verbose:
            subprocess.run(cmd, cwd=input_dir, check=True)
        else:
            subprocess.run(cmd, cwd=input_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if verbose: print("TRACK simulation completed successfully.")
        if output_dir != None:
            os.makedirs(output_dir, exist_ok=True)
            move_output_files(output_dir)
            if verbose: print("TRACK simulation outputs moved successfully")
    except subprocess.CalledProcessError as e:
        if verbose: print("TRACK simulation failed.")
        raise e

#shutil.copy(src, dst)

def move_output_files(dest_dir):
    for output_file in output_list:
        try:
            shutil.move(output_file, os.path.join(dest_dir, output_file)) 
        except FileNotFoundError:
            print(f"Error: Source file '{output_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

def clean_results(input_dir="."):
    print(f"Cleanup previous outputs")
    for output_file in output_list:
        try:
            os.remove(os.path.join(input_dir, output_file))
            print(f"    Successfully deleted {output_file}")
        except FileNotFoundError:
            print(f"    Error: {output_file} not found.")
        except Exception as e:
            print(f"    Error deleting {output_file}: {e}")

