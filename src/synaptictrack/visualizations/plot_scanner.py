import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

from synaptictrack.utils import gaussian
from synaptictrack.visualizations.plot_phasespace import phasespace_plot

def wire_scanner_plot(x_pos, x_curr, popt_x, y_pos, y_curr, popt_y):
    """
    Plot wire scanner data for X and Y axes with Gaussian fits.

    Args:
        x_pos (array): X positions [mm]
        x_curr (array): X currents [A]
        popt_x (array): Parameters of Gaussian fit for X
        y_pos (array): Y positions [mm]
        y_curr (array): Y currents [A]
        popt_y (array): Parameters of Gaussian fit for Y
    """

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

def alison_scanner_plot(x, xp, x_center, xp_center, current, density=True, bins=150, projection=True):
    """
    Plot 2D phase space from Alison scanner data with optional projections.
    
    Args:
        x (array): Position in mm
        xp (array): Divergence in mrad
        x_center (float): Beam center in x
        xp_center (float): Beam center in x'
        current (array): Current weights
        density (bool): Plot density map if True, else scatter
        bins (int): Number of bins for histogram
        projection (bool): Show projection histograms
    """
    fig = plt.figure(figsize=(8, 6))

    # Setup plot grid
    gs = gridspec.GridSpec(2, 4, width_ratios=[4, 1, 0.2, 0.2], 
                           height_ratios=[1, 4],
                           hspace=0.15, wspace=0.15)

    ax_main = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax_main)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax_main)

    # Main 2D phase space plot
    if density:
        h2d = ax_main.hist2d(x, xp, bins=bins, weights=current, cmap='viridis', density=False)
        cax = fig.add_subplot(gs[1, 2])  # Colorbar axis
        fig.colorbar(h2d[3], cax=cax, 
                     #ax=ax_main, 
                     label='Current [A]')
    else:
        ax_main.scatter(x, xp, c=current, cmap='plasma', s=2)

    ax_main.plot(x_center, xp_center, 'ro', markersize=6, label="Beam Center")
    ax_main.legend()
    ax_main.set_xlabel(r"$x$ [mm]")
    ax_main.set_ylabel(r"$x'$ [mrad]")
    ax_main.set_title("Alison Scanner Phase Space")

    # Projections (weighted histograms)
    if projection:
        # Top (x projection)
        hist_x, xedges = np.histogram(x, bins=bins, weights=current)
        ax_histx.plot((xedges[:-1] + xedges[1:]) / 2, hist_x, drawstyle='steps-mid', color='orange')
        ax_histx.set_yticks([])
        ax_histx.tick_params(labelbottom=False)
        ax_histx.grid(True)

        # Right (x' projection)
        hist_xp, xpedges = np.histogram(xp, bins=bins, weights=current)
        ax_histy.plot(hist_xp, (xpedges[:-1] + xpedges[1:]) / 2, drawstyle='steps-mid', color='orange')
        ax_histy.set_xticks([])
        ax_histy.tick_params(labelleft=False)
        ax_histy.grid(True)

    else:
        ax_histx.axis('off')
        ax_histy.axis('off')

