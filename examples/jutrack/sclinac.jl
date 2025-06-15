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

# Drift elements

D01 = DRIFT(name="D01", len=0.19440, RApertues=(0.05, 0.05))
D02 = DRIFT(name="D02", len=0.09050, RApertues=(0.05, 0.05))
D03 = DRIFT(name="D03", len=0.15500, RApertues=(0.06, 0.06))
D04 = DRIFT(name="D04", len=0.36900, RApertues=(0.06, 0.06))
D05 = DRIFT(name="D05", len=0.23100, RApertues=(0.06, 0.06))
D06 = DRIFT(name="D06", len=0.10000, RApertues=(0.06, 0.06))
D07 = DRIFT(name="D07", len=0.19655, RApertues=(0.06, 0.06))
D08 = DRIFT(name="D08", len=1.09945, RApertues=(0.06, 0.06))
D09 = DRIFT(name="D09", len=0.35600, RApertues=(0.06, 0.06))
D10 = DRIFT(name="D10", len=0.18260, RApertues=(0.06, 0.06))
D11 = DRIFT(name="D11", len=0.03540, RApertues=(0.06, 0.06))
D12 = DRIFT(name="D12", len=0.04145, RApertues=(0.06, 0.06))
D13 = DRIFT(name="D13", len=0.22855, RApertues=(0.06, 0.06))
D14 = DRIFT(name="D14", len=0.24700, RApertues=(0.06, 0.06))
D15 = DRIFT(name="D15", len=1.05300, RApertues=(0.06, 0.06))
D16 = DRIFT(name="D16", len=0.08000, RApertues=(0.06, 0.06))
D17 = DRIFT(name="D17", len=0.18955, RApertues=(0.06, 0.06))
D18 = DRIFT(name="D18", len=0.82445, RApertues=(0.06, 0.06))
D19 = DRIFT(name="D19", len=0.25400, RApertues=(0.06, 0.06))
D20 = DRIFT(name="D20", len=0.24600, RApertues=(0.06, 0.06))
D21 = DRIFT(name="D21", len=0.25000, RApertues=(0.06, 0.06))
D22 = DRIFT(name="D22", len=0.24665, RApertues=(0.06, 0.06))
D23 = DRIFT(name="D23", len=0.13665, RApertues=(0.06, 0.06))

# Magnetostatic elements
Q01 = QUAD(name="Q01", len=0.1440, k1=  0.000000)
Q02 = QUAD(name="Q02", len=0.0767, k1=-45.299486)

# Electrostatic elements
EQ01 = QUAD(name="EQ01", len=0.100, k1=-22.637170)
EQ02 = QUAD(name="EQ02", len=0.100, k1= 39.449774)
EQ03 = QUAD(name="EQ03", len=0.100, k1=-20.850502)
EQ04 = QUAD(name="EQ04", len=0.100, k1= 19.183142)
EQ05 = QUAD(name="EQ05", len=0.100, k1=-13.956586)
EQ06 = QUAD(name="EQ06", len=0.100, k1= -8.521332)
EQ07 = QUAD(name="EQ07", len=0.100, k1=-23.241152)
EQ08 = QUAD(name="EQ08", len=0.100, k1= 44.553717)
EQ09 = QUAD(name="EQ09", len=0.100, k1=-26.610679)
EQ10 = QUAD(name="EQ10", len=0.100, k1= 31.813487)
EQ11 = QUAD(name="EQ11", len=0.100, k1=-33.070472)
EQ12 = QUAD(name="EQ12", len=0.100, k1= -3.335603)
EQ13 = QUAD(name="EQ13", len=0.100, k1=  3.612444)
EQ14 = QUAD(name="EQ14", len=0.100, k1=-11.351924)
EQ15 = QUAD(name="EQ15", len=0.100, k1= 18.562108)
EQ16 = QUAD(name="EQ16", len=0.100, k1=-43.886285)
EQ17 = QUAD(name="EQ17", len=0.100, k1= 49.581179)

# Bending Magnet
B1 = SBEND(name="B1", len=0.62831853, angle=deg2rad(-90.0), e1=deg2rad(25.4495), e2=deg2rad(25.4495))
B1 = SBEND(name="B2", len=1.0210, angle=deg2rad(-90.0), e1=0.0, e2=0.0)

# Beam Diagnostics Marker
WS01 = MARKER(name="WS01")
WS02 = MARKER(name="WS02")
WS03 = MARKER(name="WS03")
WS04 = MARKER(name="WS04")
AS01 = MARKER(name="AS01")

# LEBT Beamline
LEBT = [D01, Q01, D02, B01, D03, D04, WS01, D05, EQ01, D06, EQ02, D06, EQ03, D07, D08, AS01, D09, EQ04, D06, EQ05, D06, EQ06, D10, D11, B02, D12, D13, EQ07, D06, EQ08, D06, EQ09, D14, WS02, D15, EQ10, D16, EQ11, D17, D18, WS03, D19, EQ12, D16, EQ13, D20, WS04, D19, EQ14, D16, EQ15, D21, EQ16, D16, EQ17, D22, Q02, D23]


# Space-charge enabled elements

# Drift elements
D01SC = DRIFT_SC(name="D01SC", len=0.1944, a=0.05, b=0.05, Nl=15, Nm=15, Nsteps=10)
D02SC = DRIFT_SC(name="D02SC", len=0.09050, a=0.05, b=0.05, Nl=15, Nm=15, Nsteps=10)
D03SC = DRIFT_SC(name="D03SC", len=0.15500, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D04SC = DRIFT_SC(name="D04SC", len=0.36900, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D05SC = DRIFT_SC(name="D05SC", len=0.23100, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D06SC = DRIFT_SC(name="D06SC", len=0.10000, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D07SC = DRIFT_SC(name="D07SC", len=0.19655, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D08SC = DRIFT_SC(name="D08SC", len=1.09945, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D09SC = DRIFT_SC(name="D09SC", len=0.35600, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D10SC = DRIFT_SC(name="D10SC", len=0.18260, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D11SC = DRIFT_SC(name="D11SC", len=0.03540, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D12SC = DRIFT_SC(name="D12SC", len=0.04145, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D13SC = DRIFT_SC(name="D13SC", len=0.22855, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D14SC = DRIFT_SC(name="D14SC", len=0.24700, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D15SC = DRIFT_SC(name="D15SC", len=1.05300, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D16SC = DRIFT_SC(name="D16SC", len=0.08000, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D17SC = DRIFT_SC(name="D17SC", len=0.18955, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D18SC = DRIFT_SC(name="D18SC", len=0.82445, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D19SC = DRIFT_SC(name="D19SC", len=0.25400, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D20SC = DRIFT_SC(name="D20SC", len=0.24600, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D21SC = DRIFT_SC(name="D21SC", len=0.25000, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D22SC = DRIFT_SC(name="D22SC", len=0.24665, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
D23SC = DRIFT_SC(name="D23SC", len=0.13665, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)


Q1SC = QUAD_SC(name="Q1SC", len=0.144, k1=, a=0.042, b=0.042, Nl=15, Nm=15, Nsteps=10)
# Magnetostatic elements
Q01SC = QUAD_SC(name="Q01SC", len=0.1440, k1=  0.000000, a=0.042, b=0.042, Nl=15, Nm=15, Nsteps=10)
Q02SC = QUAD_SC(name="Q02SC", len=0.0767, k1=-45.299486, a=0.042, b=0.042, Nl=15, Nm=15, Nsteps=10)

# Electrostatic elements
EQ01SC = QUAD_SC(name="EQ01SC", len=0.100, k1=-22.637170, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ02SC = QUAD_SC(name="EQ02SC", len=0.100, k1= 39.449774, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ03SC = QUAD_SC(name="EQ03SC", len=0.100, k1=-20.850502, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ04SC = QUAD_SC(name="EQ04SC", len=0.100, k1= 19.183142, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ05SC = QUAD_SC(name="EQ05SC", len=0.100, k1=-13.956586, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ06SC = QUAD_SC(name="EQ06SC", len=0.100, k1= -8.521332, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ07SC = QUAD_SC(name="EQ07SC", len=0.100, k1=-23.241152, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ08SC = QUAD_SC(name="EQ08SC", len=0.100, k1= 44.553717, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ09SC = QUAD_SC(name="EQ09SC", len=0.100, k1=-26.610679, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ10SC = QUAD_SC(name="EQ10SC", len=0.100, k1= 31.813487, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ11SC = QUAD_SC(name="EQ11SC", len=0.100, k1=-33.070472, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ12SC = QUAD_SC(name="EQ12SC", len=0.100, k1= -3.335603, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ13SC = QUAD_SC(name="EQ13SC", len=0.100, k1=  3.612444, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ14SC = QUAD_SC(name="EQ14SC", len=0.100, k1=-11.351924, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ15SC = QUAD_SC(name="EQ15SC", len=0.100, k1= 18.562108, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ16SC = QUAD_SC(name="EQ16SC", len=0.100, k1=-43.886285, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ17SC = QUAD_SC(name="EQ17SC", len=0.100, k1= 49.581179, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)

# Bending magnets
B1SC = SBEND_SC(name="B1SC", len=0.62831853, angle=deg2rad(-90.0), e1=deg2rad(25.4495), e2=deg2rad(25.4495), a=0.18, b=0.09, Nl=15, Nm=15, Nsteps=10)
B2SC = SBEND_SC(name="B2SC", len=1.0210, angle=deg2rad(-90.0), e1=0.0, e2=0.0, a=0.18, b=0.09, Nl=15, Nm=15, Nsteps=10)

# LEBT beamline with space charge
LEBTSC = [D01SC, Q01SC, D02SC, B01SC, D03SC, D04SC, WS01, D05SC, EQ01SC, D06SC, EQ02SC, D06SC, EQ03SC, D07SC, D08SC, AS01, D09SC, EQ04SC, D06SC, EQ05SC, D06SC, EQ06SC, D10SC, D11SC, B02SC, D12SC, D13SC, EQ07SC, D06SC, EQ08SC, D06SC, EQ09SC, D14SC, WS02, D15SC, EQ10SC, D16SC, EQ11SC, D17SC, D18SC, WS03, D19SC, EQ12SC, D16SC, EQ13SC, D20SC, WS04, D19SC, EQ14SC, D16SC, EQ15SC, D21SC, EQ16SC, D16SC, EQ17SC, D22SC, Q02SC, D23SC]

