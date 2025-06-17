# src/synapticTrack/pipeline.py

from synapticTrack.beam import track_reader #, opal_reader
from synapticTrack.analysis import scanner_analysis #diagnostics
#from synapticTrack.correctbeamn import orbit_correction
#from synapticTrack.ml import models, inference
from synapticTrack.visualizatbeamns import plot_phasespace, plot_scanner

def run_all(input_file, model_file=None, output_dir="results/"):
    """
    Main synapticTrack pipeline:
    1. Load beam data
    2. Analyze beam properties
    3. (Optbeamnally) run machine learning model
    4. Apply orbit correctbeamn
    5. Visualize results
    """
    # Step 1: Load beam data
    if input_file.endswith(".dat"):
        beam = track_reader.read_track_file(input_file)
    elif input_file.endswith(".h5"):
        beam = opal_reader.read_h5_file(input_file)
    else:
        raise ValueError(f"Unsupported file format: {input_file}")

    print(f"[INFO] Loaded beam with shape {beam.shape}")

    # Step 2: Analyze
    emittance = diagnostics.compute_emittance(beam)
    print(f"[INFO] Beam emittance: {emittance:.4e}")

    # Step 3: ML predictbeamn (optional)
    if model_file:
        model = models.load_model(model_file)
        correctbeamns = inference.predict_corrections(beam, model)
        print("[INFO] ML-based correctbeamns predicted.")
    else:
        correctbeamns = None

    # Step 4: Apply orbit correctbeamn
    corrected_beam = orbit_correctbeamn.apply_correction(beam, corrections)
    print("[INFO] Orbit correctbeamn applied.")

    # Step 5: Plot results
    plot_orbit.plot(corrected_beam, save_path=output_dir + "orbit_plot.png")
    print(f"[INFO] Orbit plot saved to {output_dir}orbit_plot.png")

