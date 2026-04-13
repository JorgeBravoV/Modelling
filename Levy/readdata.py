import numpy as np

import matplotlib.pyplot as plt

L=20
N_pasos=100000
alpha_0=2.2
alpha_f=2.4
delta_alpha=0.01
D=3

# Read the data file
data = np.loadtxt(f'Results/Levy/Data/{D}D/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.txt', skiprows=1)

# Extract columns
alphas = data[:, 0]
n_steps = data[:, 1]
errorbars = data[:, 2]

# Create the plot
plt.figure(figsize=(10, 6))
plt.errorbar(alphas, n_steps, yerr=errorbars, fmt='o', capsize=5, capthick=2)
plt.xlabel('Alpha')
plt.ylabel('Number of Steps')
plt.title(f'L{L} - Npasos{N_pasos} - {D}D')
plt.grid(True, alpha=0.3)
plt.savefig(f'Results/Levy/Plots/{D}D/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.png', dpi=300, bbox_inches='tight')
plt.show()