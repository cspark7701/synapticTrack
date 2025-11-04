import numpy as np
import scipy as sp
import pandas as pd

from scipy.optimize import curve_fit

from synapticTrack.utils import gaussian
from synapticTrack.visualizations import wire_scanner_plot, allison_scanner_plot

def _weighted_rms_and_center(values, weights):
    """Return center and RMS."""
    average = np.sum(values * weights) / np.sum(weights)
    variance = np.sum(weights * (values - average)**2) / np.sum(weights)
    return average, np.sqrt(variance)

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

    # Compute RMS beam sizes
    x_center, sigma_x = _weighted_rms_and_center(x, ix)
    y_center, sigma_y = _weighted_rms_and_center(y, iy)

    # Gaussian fit
    popt_x, _ = curve_fit(gaussian, x, ix, 
                          p0=[np.max(ix), x_center, sigma_x, 0])
    popt_y, _ = curve_fit(gaussian, y, iy, 
                          p0=[np.max(ix), y_center, sigma_y, 0])

    x_center_fit = popt_x[1]
    y_center_fit = popt_y[1]
    sigma_x_fit = popt_x[2]
    sigma_y_fit = popt_y[2]

    if plot:
        wire_scanner_plot(x, ix, x_center, popt_x, y, iy, y_center, popt_y, filename)

    results = {
        "x_center": x_center,
        "y_center": y_center,
        "sigma_x": sigma_x,
        "sigma_y": sigma_y,
        "gaussian_fit_x_center": x_center_fit,
        "gaussian_fit_y_center": y_center_fit,
        "gaussian_fit_sigma_x": sigma_x_fit,
        "gaussian_fit_sigma_y": sigma_y_fit
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
    x_current = beamas.x_current

    # Compute beam center and RMS
    x_center, sigma_x = _weighted_rms_and_center(x, x_current)
    xp_center, sigma_xp = _weighted_rms_and_center(xp, x_current)

    # Compute weighted covariance between x and xp
    x_centered = x - x_center
    xp_centered = xp - xp_center
    covariance_x_xp = np.sum(x_current * x_centered * xp_centered) / np.sum(x_current)

    emittance_rms = np.sqrt(sigma_x**2 * sigma_xp**2 - covariance_x_xp**2)

    # Estimate emittance (geometric)
    emittance_geometric = sigma_x * sigma_xp  # [mm·mrad]

    # Gaussian fit
    popt_x, _ = curve_fit(gaussian, x, x_current,
                          p0=[np.max(x_current), x_center, sigma_x, 0])
    popt_xp, _ = curve_fit(gaussian, xp, x_current,
                          p0=[np.max(x_current), xp_center, sigma_xp, 0])

    x_center_fit = popt_x[1]
    xp_center_fit = popt_xp[1]
    sigma_x_fit = popt_x[2]
    sigma_xp_fit = popt_xp[2]


    if plot:
        allison_scanner_plot(x, xp, x_center, xp_center, x_current, density, bins, projection, filename)

    return {
        "x_center": x_center,
        "xp_center": xp_center,
        "sigma_x": sigma_x,
        "sigma_xp": sigma_xp,
        "gaussian_fit_x_center": x_center_fit,
        "gaussian_fit_xp_center": xp_center_fit,
        "gaussian_fit_sigma_x": sigma_x_fit,
        "gaussian_fit_sigma_xp": sigma_xp_fit,
        "covariance_x_xp": covariance_x_xp,
        "emittance_rms": emittance_rms,
        "emittance_geometric": emittance_geometric
    }

