import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from synaptictrack.beam import Twiss

def phasespace_plot(x, xp, x_center=None, y_center=None, xyrange=None, title=None, xlabel=None, ylabel=None, nbins=200, projection=1, ellipse=False, density=True, cmap='viridis', figname=None):
    """
    Generates a phase space plot with projections.

    Args:
        x (array-like): x-coordinates.
        xp (array-like): x' (divergence) coordinates.
        xyrange (list, optional): [xmin, xmax, ymin, ymax]. Defaults to [-10, 10, -10, 10].
        title (str, optional): Plot title. Defaults to None.
        xlabel (str, optional): x-axis label. Defaults to None.
        ylabel (str, optional): y-axis label. Defaulst to None.
        nbins (int, optional): Number of bins for histograms. Defaults to 200.
        projection (int, optional) : places of projection plots (outside(0)or inside(1)) Default is outside.
        density (bool, optional): Use hist2d (True) or scatter (False). Defaults to True.
        cmap (str, optional): Colormap for hist2d. Defaults to 'viridis'.
        figname (str, optional): Filename to save the figure. Defaults to None.
    """
    # Default plot range
    if xyrange is None:
        xyrange = [-10, 10, -10, 10]
    xmin, xmax, ymin, ymax = xyrange

    # Setup figure and GridSpec
    fig = plt.figure(figsize=(8, 6))
    if density:
        gs = gridspec.GridSpec(2, 5, width_ratios=[4, 1, 0.2, 0.2, 0.2],  # Added columns for colorbar space
                               height_ratios=[1, 4],
                               hspace=0.15,
                               wspace=0.15)
        cax = fig.add_subplot(gs[1, 2])  # Colorbar axis
    else:
        gs = gridspec.GridSpec(2, 4, width_ratios=[4, 1, 0.2, 0.2],  # Added columns for colorbar space
                               height_ratios=[1, 4],
                               hspace=0.15,
                               wspace=0.15)

    # Arrange subplots
    if projection == 0:
        ax_main = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax_main)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax_main)
    else:
        ax_main = fig.add_subplot(gs[1, 0])
        ax_histx = ax_main.twinx()
        ax_histy = ax_main.twiny()

    # Main plot
    if density:
        h, xedges, yedges, im = ax_main.hist2d(x, xp, bins=nbins, cmap=cmap,
                                              range=[[xmin, xmax], [ymin, ymax]],
                                              density=True)  # Added density=True
        fig.colorbar(im, cax=cax, label='Density') #Associate the colorbar to the hist2d
    else:
        ax_main.scatter(x, xp, s=3)

    if x_center is not None and y_center is not None:
        ax_main.plot(x_center, y_center, 'ro', markersize=6, label="Beam Center")
        ax_main.legend()
        
    ax_main.set_xlabel(xlabel, fontsize=14)
    ax_main.set_ylabel(ylabel, fontsize=14)
    ax_main.set_xlim([xmin, xmax])
    ax_main.set_ylim([ymin, ymax])
    ax_main.grid(True)

    # Top projection
    ax_histx.hist(x, bins=nbins, histtype='step', color='orange')
    ax_histx.grid(True)
    ax_histx.set_yticks([])
    ax_histx.tick_params(labelbottom=False)    

    # Right projection
    ax_histy.hist(xp, bins=nbins, range=(ymin, ymax), orientation='horizontal', histtype='step', color='orange')
    ax_histy.grid(True)
    ax_histy.set_xticks([])
    ax_histy.tick_params(labelleft=False)
    
    if projection != 0:
        ax_histx.set_ylim(0, ax_histx.get_ylim()[1]*projection)
        ax_histy.set_xlim(0, ax_histy.get_xlim()[1]*projection)

    if ellipse:
        plot_ellipse_from_twiss(x, xp, ax_main)

    # Set title
    if title:
        ax_histx.set_title(title, fontsize=14)

    # Save figure
    if figname:
        plt.savefig(figname, dpi=fig.dpi)

def compute_mahalanobis_squared(x, xp, twiss_param):
    emit = twiss_param['emittance']
    alpha = twiss_param['alpha']
    beta = twiss_param['beta']
    gamma = twiss_param['gamma']

    return (gamma * x**2 + 2 * alpha * x * xp + beta * xp**2) / emit

def get_threshold(d_squared, percentile=0.9):
    sorted_vals = np.sort(d_squared)
    index = int(percentile * len(sorted_vals))
    return sorted_vals[index]

def plot_percentile_ellipse(x, xp, ax=None, percentile=0.9, npts=200, color='oragne'):
    twiss_param = Twiss.compute_twiss(x, xp)
    
    emit = twiss_param["emittance"]
    alpha = twiss_param["alpha"]
    beta = twiss_param["beta"]
    gamma = twiss_param['gamma']

    # Compute Mahalanobis distance for all particles
    d2 = compute_mahalanobis_squared(x, xp, twiss_param)
    threshold = get_threshold(d2, percentile)

    # Scale emittance to match desired contour
    scaled_emit = emit * threshold

    # Ellipse parametric plot
    theta = np.linspace(0, 2 * np.pi, npts)
    u = np.sqrt(scaled_emit * beta) * np.cos(theta)
    up = -np.sqrt(scaled_emit / beta) * (alpha * np.cos(theta) + np.sin(theta))

    if ax is not None:
        ax.plot(u, up, '--', color=color, label=f"{int(percentile * 100)}% Ellipse")
    else:
        plt.figure(figsize=(6, 5))
        plt.plot(u, up, '-', color='orange', label='Twiss Ellipse')
        plt.xlabel("u [mm]")
        plt.ylabel("u' [mrad]")
        plt.grid(True)
        plt.axis('equal')
        plt.legend()
        plt.tight_layout()

def plot_ellipse_from_twiss(x, xp, ax=None, npts=200):
    """
    Plot the phase space ellipse from computed Twiss parameters.

    Args:
        x (array-like): Position values
        xp (array-like): Divergence or angle values
        ax (matplotlib.axes.Axes or None): Axis to plot on. If None, uses plt.
        npts (int): Number of points on the ellipse
    """
    twiss_param = Twiss.compute_twiss(x, xp)

    emit = twiss_param["emittance"]
    alpha = twiss_param["alpha"]
    beta = twiss_param["beta"]

    theta = np.linspace(0, 2 * np.pi, npts)
    u = np.sqrt(emit * beta) * np.cos(theta)
    up = -np.sqrt(emit / beta) * (alpha * np.cos(theta) + np.sin(theta))

    if ax is not None:
        ax.plot(u, up, '-', color='orange', label='Twiss Ellipse')
    else:
        plt.figure(figsize=(6, 5))
        plt.plot(u, up, '-', color='orange', label='Twiss Ellipse')
        plt.xlabel("u [mm]")
        plt.ylabel("u' [mrad]")
        plt.grid(True)
        plt.axis('equal')
        plt.legend()
        plt.tight_layout()

