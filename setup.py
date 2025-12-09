from setuptools import setup, find_packages

PACKAGE_NAME = "synapticTrack"

setup(
    name="synapticTrack",
    version="0.1.0",
    description="Heavy Ion Linac Orbit Correction & Beam Dynamics Framework with ML",
    author="Chong Shik Park",
    author_email="kuphy@korea.ac.kr",
    url="https://github.com/your-org/synapticTrack",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.9.1",
        "gymnasium>=1.2.2",
        "numpy>=1.20",
        "scipy>=1.7",
        "matplotlib>=3.4",
        "pandas>=1.3",
        "tqdm>=4.62",
        "h5py>=3.0",
        "pymongo>=4.0",
        "typer[all]>=0.9",
        "scikit-learn>=1.0",
        "periodictable>2.0",
        "nbstripout>0.8.1"
    ],
    entry_points={
        "console_scripts": [
            "synapticTrack = synapticTrack.cli:app"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

