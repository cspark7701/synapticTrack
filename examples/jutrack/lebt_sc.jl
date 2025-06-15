using JuTrack

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

# Magnetostatic elements
Q01SC = KQUAD_SC(name="Q01SC", len=0.1440, k1=  0.000000, a=0.042, b=0.042, Nl=15, Nm=15, Nsteps=10)
Q02SC = KQUAD_SC(name="Q02SC", len=0.0767, k1=-45.299486, a=0.042, b=0.042, Nl=15, Nm=15, Nsteps=10)

# Electrostatic elements
EQ01SC = KQUAD_SC(name="EQ01SC", len=0.100, k1=-22.637170, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ02SC = KQUAD_SC(name="EQ02SC", len=0.100, k1= 39.449774, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ03SC = KQUAD_SC(name="EQ03SC", len=0.100, k1=-20.850502, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ04SC = KQUAD_SC(name="EQ04SC", len=0.100, k1= 19.183142, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ05SC = KQUAD_SC(name="EQ05SC", len=0.100, k1=-13.956586, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ06SC = KQUAD_SC(name="EQ06SC", len=0.100, k1= -8.521332, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ07SC = KQUAD_SC(name="EQ07SC", len=0.100, k1=-23.241152, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ08SC = KQUAD_SC(name="EQ08SC", len=0.100, k1= 44.553717, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ09SC = KQUAD_SC(name="EQ09SC", len=0.100, k1=-26.610679, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ10SC = KQUAD_SC(name="EQ10SC", len=0.100, k1= 31.813487, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ11SC = KQUAD_SC(name="EQ11SC", len=0.100, k1=-33.070472, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ12SC = KQUAD_SC(name="EQ12SC", len=0.100, k1= -3.335603, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ13SC = KQUAD_SC(name="EQ13SC", len=0.100, k1=  3.612444, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ14SC = KQUAD_SC(name="EQ14SC", len=0.100, k1=-11.351924, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ15SC = KQUAD_SC(name="EQ15SC", len=0.100, k1= 18.562108, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ16SC = KQUAD_SC(name="EQ16SC", len=0.100, k1=-43.886285, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)
EQ17SC = KQUAD_SC(name="EQ17SC", len=0.100, k1= 49.581179, a=0.06, b=0.06, Nl=15, Nm=15, Nsteps=10)

# Bending magnets
B01SC = SBEND_SC(name="B01SC", len=0.62831853, angle=deg2rad(-90.0), e1=deg2rad(25.4495), e2=deg2rad(25.4495), a=0.18, b=0.09, Nl=15, Nm=15, Nsteps=10)
B02SC = SBEND_SC(name="B02SC", len=1.0210, angle=deg2rad(-90.0), e1=0.0, e2=0.0, a=0.18, b=0.09, Nl=15, Nm=15, Nsteps=10)

# Beam Diagnostics Marker
WS01 = MARKER(name="WS01")
WS02 = MARKER(name="WS02")
WS03 = MARKER(name="WS03")
WS04 = MARKER(name="WS04")
AS01 = MARKER(name="AS01")

# LEBT beamline with space charge
LEBTSC = [D01SC, Q01SC, D02SC, B01SC, D03SC, D04SC, WS01, D05SC, EQ01SC, D06SC, EQ02SC, D06SC, EQ03SC, D07SC, D08SC, AS01, D09SC, EQ04SC, D06SC, EQ05SC, D06SC, EQ06SC, D10SC, D11SC, B02SC, D12SC, D13SC, EQ07SC, D06SC, EQ08SC, D06SC, EQ09SC, D14SC, WS02, D15SC, EQ10SC, D16SC, EQ11SC, D17SC, D18SC, WS03, D19SC, EQ12SC, D16SC, EQ13SC, D20SC, WS04, D19SC, EQ14SC, D16SC, EQ15SC, D21SC, EQ16SC, D16SC, EQ17SC, D22SC, Q02SC, D23SC]

