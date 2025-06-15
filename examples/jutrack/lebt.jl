using JuTrack

# Drift elements

D01 = DRIFT(name="D01", len=0.19440, RApertures=[0.05, 0.05])
D02 = DRIFT(name="D02", len=0.09050, RApertures=[0.05, 0.05])
D03 = DRIFT(name="D03", len=0.15500, RApertures=[0.06, 0.06])
D04 = DRIFT(name="D04", len=0.36900, RApertures=[0.06, 0.06])
D05 = DRIFT(name="D05", len=0.23100, RApertures=[0.06, 0.06])
D06 = DRIFT(name="D06", len=0.10000, RApertures=[0.06, 0.06])
D07 = DRIFT(name="D07", len=0.19655, RApertures=[0.06, 0.06])
D08 = DRIFT(name="D08", len=1.09945, RApertures=[0.06, 0.06])
D09 = DRIFT(name="D09", len=0.35600, RApertures=[0.06, 0.06])
D10 = DRIFT(name="D10", len=0.18260, RApertures=[0.06, 0.06])
D11 = DRIFT(name="D11", len=0.03540, RApertures=[0.06, 0.06])
D12 = DRIFT(name="D12", len=0.04145, RApertures=[0.06, 0.06])
D13 = DRIFT(name="D13", len=0.22855, RApertures=[0.06, 0.06])
D14 = DRIFT(name="D14", len=0.24700, RApertures=[0.06, 0.06])
D15 = DRIFT(name="D15", len=1.05300, RApertures=[0.06, 0.06])
D16 = DRIFT(name="D16", len=0.08000, RApertures=[0.06, 0.06])
D17 = DRIFT(name="D17", len=0.18955, RApertures=[0.06, 0.06])
D18 = DRIFT(name="D18", len=0.82445, RApertures=[0.06, 0.06])
D19 = DRIFT(name="D19", len=0.25400, RApertures=[0.06, 0.06])
D20 = DRIFT(name="D20", len=0.24600, RApertures=[0.06, 0.06])
D21 = DRIFT(name="D21", len=0.25000, RApertures=[0.06, 0.06])
D22 = DRIFT(name="D22", len=0.24665, RApertures=[0.06, 0.06])
D23 = DRIFT(name="D23", len=0.13665, RApertures=[0.06, 0.06])

# Magnetostatic elements
Q01 = KQUAD(name="Q01", len=0.1440, k1=  0.000000)
Q02 = KQUAD(name="Q02", len=0.0767, k1=-45.299486)

# Electrostatic elements
EQ01 = KQUAD(name="EQ01", len=0.100, k1=-22.637170)
EQ02 = KQUAD(name="EQ02", len=0.100, k1= 39.449774)
EQ03 = KQUAD(name="EQ03", len=0.100, k1=-20.850502)
EQ04 = KQUAD(name="EQ04", len=0.100, k1= 19.183142)
EQ05 = KQUAD(name="EQ05", len=0.100, k1=-13.956586)
EQ06 = KQUAD(name="EQ06", len=0.100, k1= -8.521332)
EQ07 = KQUAD(name="EQ07", len=0.100, k1=-23.241152)
EQ08 = KQUAD(name="EQ08", len=0.100, k1= 44.553717)
EQ09 = KQUAD(name="EQ09", len=0.100, k1=-26.610679)
EQ10 = KQUAD(name="EQ10", len=0.100, k1= 31.813487)
EQ11 = KQUAD(name="EQ11", len=0.100, k1=-33.070472)
EQ12 = KQUAD(name="EQ12", len=0.100, k1= -3.335603)
EQ13 = KQUAD(name="EQ13", len=0.100, k1=  3.612444)
EQ14 = KQUAD(name="EQ14", len=0.100, k1=-11.351924)
EQ15 = KQUAD(name="EQ15", len=0.100, k1= 18.562108)
EQ16 = KQUAD(name="EQ16", len=0.100, k1=-43.886285)
EQ17 = KQUAD(name="EQ17", len=0.100, k1= 49.581179)

# Bending Magnet
B01 = SBEND(name="B01", len=0.62831853, angle=deg2rad(-90.0), e1=deg2rad(25.4495), e2=deg2rad(25.4495))
B02 = SBEND(name="B02", len=1.0210, angle=deg2rad(-90.0), e1=0.0, e2=0.0)

# Beam Diagnostics Marker
WS01 = MARKER(name="WS01")
WS02 = MARKER(name="WS02")
WS03 = MARKER(name="WS03")
WS04 = MARKER(name="WS04")
AS01 = MARKER(name="AS01")

# LEBT Beamline
LEBT = [D01, Q01, D02, B01, D03, D04, WS01, D05, EQ01, D06, EQ02, D06, EQ03, D07, D08, AS01, D09, EQ04, D06, EQ05, D06, EQ06, D10, D11, B02, D12, D13, EQ07, D06, EQ08, D06, EQ09, D14, WS02, D15, EQ10, D16, EQ11, D17, D18, WS03, D19, EQ12, D16, EQ13, D20, WS04, D19, EQ14, D16, EQ15, D21, EQ16, D16, EQ17, D22, Q02, D23]

