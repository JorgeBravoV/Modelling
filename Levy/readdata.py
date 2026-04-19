import numpy as np
import matplotlib.pyplot as plt

L=20
N_pasos=5000
alpha_0=2.0
alpha_f=4.0
delta_alpha=0.05
D=3

# Read the data file
data = np.loadtxt(f'Results/Levy/Data/{D}D/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.txt', skiprows=1)

# Extract columns
alphas = data[:, 0]
n_steps = data[:, 1]
errorbars = data[:, 2]

# Fit a 4-degree polynomial
coeffs = np.polyfit(alphas, n_steps, 4, w=1/errorbars)
poly = np.poly1d(coeffs)
alphas_smooth = np.linspace(alphas.min(), alphas.max(), 300)
n_steps_fit = poly(alphas_smooth)

# Find minimum alpha
min_idx = np.argmin(n_steps_fit)
min_alpha = alphas_smooth[min_idx]

# Create the plot
plt.figure(figsize=(10, 6))
plt.errorbar(
    alphas, n_steps, yerr=errorbars,
    fmt='o', markersize=4, capsize=5, capthick=2,
    label='Data', zorder=1
)
plt.plot(
    alphas_smooth, n_steps_fit, 'r-',
    linewidth=2, label='4-degree polynomial fit', zorder=3
)
plt.plot(
    min_alpha, poly(min_alpha), 'g*',
    markersize=15, label=f'Minimum at α={min_alpha:.3f}', zorder=4
)
plt.xlabel('α', fontsize=20)
plt.ylabel('Number of Steps', fontsize=20)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=20)
plt.tick_params(labelsize=20)
plt.savefig(
    f'Results/Levy/Plots/{D}D/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.png',
    dpi=300, bbox_inches='tight'
)
plt.show()

print(f"Minimum alpha: {min_alpha:.3f}")