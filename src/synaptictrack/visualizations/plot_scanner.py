import numpy as np
import matplotlib.pyplot as plt

from synaptictrack.utils import gaussian

def wire_scanner_plot(x_pos, x_curr, popt_x, y_pos, y_curr, popt_y):
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


def alison_scanner_plot(x, xp, x_center, xp_center, current, density, bins):
    plt.figure(figsize=(7, 5))
    if density:
        # plot density map
        counts, xedges, yedges, img = plt.hist2d(
            x, xp, bins=bins, weights=current,
            cmap='plasma', density=False
        )
        plt.colorbar(label='Current [A]')
    else:
        plt.scatter(x, xp, c=current, cmap='viridis', s=5)
        plt.colorbar(label='Current [A]')

    # Plot beam center
    plt.plot(x_center, xp_center, 'ro', markersize=6, label="Beam Center")
    plt.legend()

    plt.xlabel(r"$x$ [mm]")
    plt.ylabel(r"$x'$ [mrad]")
    plt.title("Alison Scanner Phase Space ($x$ vs $x'$)")
    plt.grid(False)
    plt.show() 
