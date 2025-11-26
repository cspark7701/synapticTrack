import numpy as np

def check_data(ws, stms, exp_x, sim_x, exp_y, sim_y):
    """
    Check centroid data for experiments and simulations
    ws: int
        the number of wire scanners
    stms: int
        the number of steering magnets
    """
    for j in range(stms):
        for i in range(ws):
            print (f"stm{j}: ws{i}: %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f"  % 
            (exp_x[i, j, 0], sim_x[i, j, 0], 
             exp_x[i, j, 1], sim_x[i, j, 1], 
             exp_y[i, j, 0], sim_y[i, j, 0], 
             exp_y[i, j, 1], sim_y[i, j, 1]))
        print ()


def compute_wire_scanner_offsets(WS, exp_x, sim_x, exp_y, sim_y, kick_zero):
    """
    Wire Scanner OFFSETS  (sim is ground-truth; exp has misalignment)
    offset = sim(ws, any steerer, zero kick) - exp(ws, any steerer, zero kick)
    Use ALL 5 steerers' zero-kick rows and average.

    WS: int
        the number of wire scanners
    exp_{i}: np array (ws, stms, :)
        experimental beam centroid
    sim_{i}: np array (ws, stms, :)
        simulation beam centroid
    kick_zero: int
        column number of the zero kick      
    """

    ws_offset_x = np.zeros(WS)
    ws_offset_y = np.zeros(WS) 

    for ws in range(WS):
        sim_zero_x = sim_x[ws, :, kick_zero]
        exp_zero_x = exp_x[ws, :, kick_zero]
        sim_zero_y = sim_y[ws, :, kick_zero]
        exp_zero_y = exp_y[ws, :, kick_zero]

        ws_offset_x[ws] = np.mean(sim_zero_x - exp_zero_x)
        ws_offset_y[ws] = np.mean(sim_zero_y - exp_zero_y)

    print("== Wire Scanner Offsets (simulation - experiment) ===")
    for ws in range(WS):
        print(f"WS{ws+1}: x_offset={ws_offset_x[ws]:+.4f},   y_offset={ws_offset_y[ws]:+.4f}")

    return (ws_offset_x, ws_offset_y)


def compute_response(WS, STEERERS, sim_arr, exp_arr, KICK_PLUS, KICK_MINUS, KICK_MAG):
    """
    Compute response matrices (per-mrad sensitivity)
    return:
       R_sim: shape (WS, STEERERS)
       R_exp: shape (WS, STEERERS)
    where R(ws,k) = (centroid(+)-centroid(-)) / (2 * kick)
    """
    R_sim = np.zeros((WS, STEERERS))
    R_exp = np.zeros((WS, STEERERS))

    for ws in range(WS):
        for k in range(STEERERS):
            dsim = (sim_arr[ws,k,KICK_PLUS] - sim_arr[ws,k,KICK_MINUS]) / 2.0
            dexp = (exp_arr[ws,k,KICK_PLUS] - exp_arr[ws,k,KICK_MINUS]) / 2.0

            R_sim[ws,k] = dsim / KICK_MAG
            R_exp[ws,k] = dexp / KICK_MAG

    return (R_sim, R_exp)


def solve_scale_factors(STEERERS, R_sim, R_exp):
    """
    Steerer scale factors (least squares)
    Solve s_k = argmin || R_sim[:,k] * s_k - R_exp[:,k] ||^2
    Closed form: s_k = (R_sim[:,k]^T R_exp[:,k]) / (R_sim[:,k]^T R_sim[:,k])
    """
    scales = np.zeros(STEERERS)
    for k in range(STEERERS):
        col_sim = R_sim[:,k]
        col_exp = R_exp[:,k]
        den = np.dot(col_sim, col_sim)
        if den < 1e-12:
            scales[k] = 1.0
        else:
            scales[k] = np.dot(col_sim, col_exp) / den
    return scales


def print_scale_factors(STEERERS, scale_x, scale_y):
    print("=== Steerer Scale Factors ===")
    for k in range(STEERERS):
        print(f"Steerer {k+1}:  s_x={scale_x[k]:.4f},   s_y={scale_y[k]:.4f}")


def print_calibration_summary(WS, STEERERS, ws_offset_x, ws_offset_y, scale_x, scale_y):
    print("=== SUMMARY ===")
    print("Wire Scanner Offsets (apply to simulation or embed into lattice):")
    for ws in range(WS):
        print(f"  WS{ws+1}:  dx={ws_offset_x[ws]:+.4f},  dy={ws_offset_y[ws]:+.4f}")

    print("\nSteerer Scale Factors (multiply TRACK FH/FV or FHkick/FVkick):")
    for k in range(STEERERS):
        print(f"  SM{k+1}:  x_scale={scale_x[k]:.4f},   y_scale={scale_y[k]:.4f}")

    print("""
Meaning:
- After applying WS offsets, simulation and experiment match at zero kick.
- After applying steerer scale factors, the ±1.1 mrad response matches experiment.
""")
