# synapticTrack

**synapticTrack** is a modular, extensible Python framework for accelerator optimization using **machine learning** techniques.

### Purpose

The framework is currently under active development to support **orbit correction and optimization** in **heavy-ion linear accelerators**, specifically focused on the **LEBT (Low Energy Beam Transport)** section.

### Features (Planned & In Progress)

- ML-based orbit correction using simulation and diagnostic data
- Interoperability with multiple beam dynamics codes:
  - [TRACK (Fortran)](https://www.phy.anl.gov/atlas/TRACK/)
  - [JuTrack (Julia)](https://github.com/cheolgyu/JuTrack.jl)
- Support for:
  - Multi-ion species (different A/Q)
  - Variable charge states and currents
  - Simulation-to-reality generalization


### Repository Structure (under construction)
synapticTrack
├── docs
│   ├── conf.py
│   ├── index.rst
│   ├── Makefile
│   ├── \_static
│   ├── synaptictrack.svg
│   ├── synaptictrack.tree
│   └── \_templates
├── examples
│   ├── analysis
│   │   ├── scanner.ipynb
│   │   └── twiss_parameters.ipynb
│   ├── demo_run.py
│   ├── jutrack
│   │   ├── beam.jl
│   │   ├── jutrack_integration.ipynb
│   │   ├── lebt.jl
│   │   ├── lebt_sc.jl
│   │   ├── r_matrix.dat
│   │   ├── sclinac.jl
│   │   ├── track.jl
│   │   └── track_sc.jl
│   ├── track
│   └── visualization
│       └── phasespace_plot.ipynb
├── LICENSE
├── pyproject.toml
├── README.md
├── setup.py
├── setup.sh
├── src
│   └── synapticTrack
│       ├── analysis
│       │   ├── __init__.py
│       │   └── scanner_analysis.py
│       ├── beam
│       │   ├── beam.py
│       │   ├── beam_scanner.py
│       │   ├── __init__.py
│       │   └── twiss.py
│       ├── cli.py
│       ├── __init__.py
│       ├── opt
│       │   └── __init__.py
│       ├── pipeline.py
│       ├── track
│       ├── utils
│       │   ├── compute_brho.py
│       │   ├── convert_bmag.py
│       │   ├── convert_equad.py
│       │   ├── __init__.py
│       │   ├── math_functions.py
│       │   └── stats.py
│       └── visualizations
│           ├── __init__.py
│           ├── plot_phasespace.py
│           └── plot_scanner.py
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── test_beam.py
    └── test_scanner.py


### Author

**Chong Shik Park**  
Accelerator Physicist / Machine Learning Researcher  
Email: [kuphy@korea.ac.kr]  
Affiliation: [Korea University, Sejong]  


### Status

 **In development** – contributions, suggestions, and feedback are welcome.



