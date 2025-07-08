import numpy as np
import scipy as sp
import pandas as pd

from scipy.optimize import curve_fit

from synapticTrack.utils import gaussian
from synapticTrack.visualizations import wire_scanner_plot, allison_scanner_plot

def _weighted_rms_and_center(values, weights):
    """Return center and RMS."""
    center = np.sum(values * weights) / np.sum(weights)
    variance = np.sum(weights * (values - center)**2) / np.sum(weights)
    return center, np.sqrt(variance)

def analyze_wire_scanner(beamws, plot=True, filename=None) -> dict:
    """
    Analyze Wire scanner data
    Computes beam profile Gaussian fit 
    Plots beam profile
    
    Args:
        beamas (BeamWS): object with x_position, x_current, y_position, y_current array
        plot (bool): whether to show phase space plot

    Returns:
        dict with results
    """

    x = beamws.x_position
    ix = beamws.x_current
    y = beamws.y_position
    iy = beamws.y_current

    # Remove repeated scans if any
    unique_x = np.unique(x, return_index=True)[1]
    unique_y = np.unique(y, return_index=True)[1]
    x, ix = x[unique_x], ix[unique_x]
    y, iy = y[unique_y], iy[unique_y]

    # Compute RMS beam sizes
    x_center, sigma_x = _weighted_rms_and_center(x, ix)
    y_center, sigma_y = _weighted_rms_and_center(y, iy)

    # Gaussian fit
    popt_x, _ = curve_fit(gaussian, x, np.abs(ix), 
                          p0=[np.max(np.abs(ix)), x_center, sigma_x, 0])
    popt_y, _ = curve_fit(gaussian, y, np.abs(iy), 
                          p0=[np.max(np.abs(iy)), y_center, sigma_y, 0])

    sigma_x_fit = np.abs(popt_x[2])
    sigma_y_fit = np.abs(popt_y[2])

    if plot:
        wire_scanner_plot(x, ix, popt_x, y, iy, popt_y, filename)

    results = {
        "x_center": x_center,
        "y_center": y_center,
        "sigma_x": sigma_x,
        "sigma_y": sigma_y,
        "gaussian_sigma_x_fit": sigma_x_fit,
        "gaussian_sigma_y_fit": sigma_y_fit
    }

    return results

def analyze_allison_scanner_2d(beamas, plot=True, bins=150, density=True, projection=True, filename=None) -> dict:
    """
    Analyze 2D Allison scanner data (phase space distribution).
    Computes beam center, beam size, divergence, and emittance.
    Plots phase space distribution (x vs xp).
    
    Args:
        beamas (BeamAS): object with x, xp, x_current arrays
        plot (bool): whether to show phase space plot
        bins (int): number of bins for histogram
        density (bool): if True, plot density map, else scatter plot

    Returns:
        dict with results
    """
    x = beamas.x
    xp = beamas.xp
    x_current = np.abs(beamas.x_current)  # take absolute current

    # Compute beam center and RMS
    x_center, sigma_x = _weighted_rms_and_center(x, x_current)
    xp_center, sigma_xp = _weighted_rms_and_center(xp, x_current)

    # Estimate emittance (geometric)
    emittance = sigma_x * sigma_xp  # [mm·mrad]

    # Gaussian fit
    popt_x, _ = curve_fit(gaussian, x, np.abs(x_current),
                          p0=[np.max(np.abs(x_current)), x_center, sigma_x, 0])
    popt_xp, _ = curve_fit(gaussian, xp, np.abs(x_current),
                          p0=[np.max(np.abs(x_current)), xp_center, sigma_xp, 0])

    sigma_x_fit = np.abs(popt_x[2])
    sigma_xp_fit = np.abs(popt_xp[2])


    if plot:
        allison_scanner_plot(x, xp, x_center, xp_center, x_current, density, bins, projection, filename)

    return {
        "x_center": x_center,
        "xp_center": xp_center,
        "sigma_x": sigma_x,
        "sigma_xp": sigma_xp,
        "gaussian_sigma_x_fit": sigma_x_fit,
        "gaussian_sigma_xp_fit": sigma_xp_fit,
        "geometric_emittance": emittance
    }

