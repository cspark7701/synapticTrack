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

def analyze_alison_scanner(beamas, plot=True):
    """
    Analyze Alison scanner data.
    Plots X current vs angle and estimates basic beam properties.
    """
    # Load data: skip first line (Korean header)

    x_pos = beamas.x_position
    x_angle = beamas.x_angle
    x_current = beamas.x_current
    hv = beamas.hv
    y_current = beamas.y_current
    
    if plot:
        # Plot current vs angle
        plt.figure(figsize=(8, 5))
        plt.scatter(x_angle, np.abs(x_current), s=3)
        plt.xlabel("X Angle [mrad]")
        plt.ylabel("Current [A] (abs)")
        plt.title("Alison Scanner X Angular Distribution")
        plt.grid(True)
        plt.show()

    # Estimate angular center and RMS
    x_center = np.sum(x_angle * np.abs(x_current)) / np.sum(np.abs(x_current))
    x_rms = np.sqrt(np.sum(np.abs(x_current) * (x_angle - x_center)**2) / np.sum(np.abs(x_current)))

    results = {
        "x_angular_center": x_center,                   # [mrad]
        "x_rms_angular_spread": x_rms                   # [mrad]
    }

    return results
