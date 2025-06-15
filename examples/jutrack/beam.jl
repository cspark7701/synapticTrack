using DelimitedFiles
using JuTrack

# Load r matrix from file
particles = readdlm("r_matrix.dat")

charge_number = 8.0
mass_number = 40.0
amu = 931.49410372
rest_mass = mass_number * amu * 1e6
energy = 10e3 + rest_mass

# Construct the beam (example values below — customize as needed)
beam = Beam(particles, energy=energy, charge=charge_number, mass=rest_mass, current=0.0)

#get_emittance!(beam::Beam)
#println(beam.emittance)
