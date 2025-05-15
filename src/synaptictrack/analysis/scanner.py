import numpy as np
import scipy as sp
import pandas as pd

from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
from matplotlib import gridspec

from synaptictrack.beam import BeamWS

def gaussian(x, a, x0, sigma, offset):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2)) + offset

def analyze_wire_scanner(beamws, plot=True):
    """
    Analyze wire scanner data from file.
    Returns: X and Y beam size (RMS, Gaussian fit)
    """

    x_pos = beamws.x_position
    x_curr = beamws.x_current
    y_pos = beamws.y_position
    y_curr = beamws.y_current

    # Remove repeated scans if any
    unique_x = np.unique(x_pos, return_index=True)[1]
    unique_y = np.unique(y_pos, return_index=True)[1]
    x_pos, x_curr = x_pos[unique_x], x_curr[unique_x]
    y_pos, y_curr = y_pos[unique_y], y_curr[unique_y]

    # Compute RMS beam sizes
    x_center = np.sum(x_pos * np.abs(x_curr)) / np.sum(np.abs(x_curr))
    y_center = np.sum(y_pos * np.abs(y_curr)) / np.sum(np.abs(y_curr))
    x_rms = np.sqrt(np.sum(np.abs(x_curr) * (x_pos - x_center)**2) / np.sum(np.abs(x_curr)))
    y_rms = np.sqrt(np.sum(np.abs(y_curr) * (y_pos - y_center)**2) / np.sum(np.abs(y_curr)))

    # Gaussian fit
    popt_x, _ = curve_fit(gaussian, x_pos, np.abs(x_curr), 
                          p0=[np.max(np.abs(x_curr)), x_center, x_rms, 0])
    popt_y, _ = curve_fit(gaussian, y_pos, np.abs(y_curr), 
                          p0=[np.max(np.abs(y_curr)), y_center, y_rms, 0])

    x_sigma_fit = np.abs(popt_x[2])
    y_sigma_fit = np.abs(popt_y[2])

    if plot:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        axs[0].plot(x_pos, np.abs(x_curr), 'o', label='Data')
        axs[0].plot(x_pos, gaussian(x_pos, *popt_x), '-', label='Gaussian Fit')
        axs[0].set_title("X Wire Scanner")
        axs[0].set_xlabel("Position [mm]")
        axs[0].set_ylabel("Current [A]")
        axs[0].legend()
        axs[0].grid(True)

        axs[1].plot(y_pos, np.abs(y_curr), 'o', label='Data')
        axs[1].plot(y_pos, gaussian(y_pos, *popt_y), '-', label='Gaussian Fit')
        axs[1].set_title("Y Wire Scanner")
        axs[1].set_xlabel("Position [mm]")
        axs[1].set_ylabel("Current [A]")
        axs[1].legend()
        axs[1].grid(True)

        plt.tight_layout()
        plt.show()

    results = {
        "x_rms": x_rms,
        "y_rms": y_rms,
        "x_gaussian_sigma": x_sigma_fit,
        "y_gaussian_sigma": y_sigma_fit
    }

    return results

def _weighted_rms(values, weights):
    center = np.sum(values * weights) / np.sum(weights)
    variance = np.sum(weights * (values - center)**2) / np.sum(weights)
    return np.sqrt(variance)

def analyze_alison_scanner_2d(beamas, plot=True, bins=150, density=True):
    """
    Analyze 2D Alison scanner data (phase space distribution).
    Computes beam size, divergence, and emittance.
    Plots phase space distribution (x vs xp).
    
    Args:
        beamas (BeamAS): object with x, xp, current arrays
        plot (bool): whether to show phase space plot

    Returns:
        dict with results
    """
    x = beamas.x
    xp = beamas.xp
    current = np.abs(beamas.x_current)  # take absolute current

    # Compute RMS beam size (σ_x) and divergence (σ_xp)
    sigma_x = _weighted_rms(x, current)
    sigma_xp = _weighted_rms(xp, current)

    # Estimate emittance (geometric)
    emittance = sigma_x * sigma_xp  # [mm·mrad]

    # Plot phase space
    if plot:
        plt.figure(figsize=(7, 5))
        if density:
            # plot density map
            counts, xedges, yedges, img = plt.hist2d(
                x, xp, bins=bins, weights=current,
                cmap='plasma', density=False
            )
        else:
            plt.scatter(x, xp, c=current, cmap='viridis', s=5)

        plt.colorbar(label='Current [A]')
        plt.xlabel(r"$x$ [mm]")
        plt.ylabel(r"$x'$ [mrad]")
        plt.title("Alison Scanner Phase Space ($x$ vs $x'$)")
        plt.grid(False)
        plt.show()

    return {
        "sigma_x_mm": sigma_x,
        "sigma_xp_mrad": sigma_xp,
        "geometric_emittance_mm_mrad": emittance
    }

