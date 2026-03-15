import numpy as np

import matplotlib.pyplot as plt

L=100
N_pasos=100000
alpha_0=2.0
alpha_f=2.2
delta_alpha=0.01

# Read the data file
data = np.loadtxt(f'Results/Levy/Data/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.txt', skiprows=1)

# Extract columns
delta_alpha = data[:, 0]
n_steps = data[:, 1]
errorbars = data[:, 2]

# Create the plot
plt.figure(figsize=(10, 6))
plt.errorbar(delta_alpha, n_steps, yerr=errorbars, fmt='o', capsize=5, capthick=2)
plt.xlabel('Delta Alpha')
plt.ylabel('Number of Steps')
plt.title(f'L{L} - Npasos{N_pasos}')
plt.grid(True, alpha=0.3)
plt.show()
plt.savefig(f'Results/Levy/Plots/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.png', dpi=300, bbox_inches='tight')