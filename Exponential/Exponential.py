import numpy as np
import matplotlib.pyplot as plt

L=25
N_pasos=1000
alpha_0=1
alpha_f=8
delta_alpha=0.05
suma=0

promedios = []
alphas = []
error = []
steps = []
n_steps = []


np.random.seed(22)

for alpha in np.arange(alpha_0,alpha_f,delta_alpha):

    for i in range(N_pasos):
        suma=0
        x0 = np.random.uniform(0, L)
        y0 = np.random.uniform(0, L)


        x_prey = np.random.uniform(0, L)
        y_prey = np.random.uniform(0, L)


        x, y = x0, y0

        distance_square = (x - x_prey)**2 + (y - y_prey)**2

        while distance_square > 1:

            sign_x = np.random.randint(0, 2)*2 - 1
            sign_y = np.random.randint(0, 2)*2 - 1

            x += np.random.exponential(alpha) * sign_x
            y += np.random.exponential(alpha) * sign_y

            x = 0 if x < 0 else L if x > L else x
            y = 0 if y < 0 else L if y > L else y
            distance_square = (x - x_prey)**2 + (y - y_prey)**2
            suma+=1
    
 
        steps.append(suma)
    
    print(f"Alpha {alpha}")
    
    promedio=(np.mean(steps))
    std = np.std(steps)
    
    alphas.append(alpha)
    promedios.append(promedio)
    error.append(std/np.sqrt(N_pasos))  # Error estándar de la media
    n_steps.append(i)
    steps.clear()  # Limpiar para la siguiente alpha

#AQUÍ HACE UNO FUERA DE SIMULACIÓN PARA PLOTEARLO
#==========================================================================================
x, y = x0, y0
distance_square = (x - x_prey)**2 + (y - y_prey)**2

positions = [(x, y)]

while distance_square > 1:
    x += np.random.exponential(alpha) * np.random.choice([-1, 1])
    y += np.random.exponential(alpha) * np.random.choice([-1, 1])

    x = np.clip(x, 0, L)
    y = np.clip(y, 0, L)

    distance_square = (x - x_prey)**2 + (y - y_prey)**2
    positions.append((x, y))

positions = np.array(positions)
print(f"Number of steps: {len(positions) - 1}")

plt.figure(figsize=(8, 8))
plt.plot(positions[:, 0], positions[:, 1], 'b-', alpha=0.7, label='Lèvy flight')
plt.plot(x0, y0, 'go', markersize=10, label='Start')
plt.plot(x_prey, y_prey, 'r*', markersize=15, label='Prey')
plt.xlim(0, L)
plt.ylim(0, L)
plt.legend()
plt.grid(True)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title(f"Exponential Flight - Number of steps: {len(positions) - 1}")
plt.show()
#===========================================================================================================
# Fit a 4-degree polynomial
errorbars = np.array(error)
alphas_array = np.array(alphas)
coeffs = np.polyfit(alphas_array, promedios, 4, w=1/errorbars)
poly = np.poly1d(coeffs)
alphas_smooth = np.linspace(alphas_array.min(), alphas_array.max(), 300)
n_steps_fit = poly(alphas_smooth)

# Find minimum alpha
min_idx = np.argmin(n_steps_fit)
min_alpha = alphas_smooth[min_idx]

# Create the plot
plt.figure(figsize=(10, 6))
plt.errorbar(
    alphas_array, promedios, yerr=errorbars,
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
    f'Results/Levy/Plots/2D/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.png',
    dpi=300, bbox_inches='tight'
)
plt.savefig(f'Exponential/Exponential.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"Minimum alpha: {min_alpha:.3f}")


plt.figure(figsize=(8, 6))
plt.plot(alphas, promedios, 'ro-', alpha=0.7)  
plt.xlabel('Alpha')
plt.ylabel('Average Number of Steps to Reach Prey')
plt.title(f'L = {L},N_pasos = {N_pasos}, alpha_range = {alpha_0}-{alpha_f}, Delta_alpha = {delta_alpha}')
plt.grid(True)
plt.savefig(f"Results/Exponential/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.png", dpi=150, bbox_inches='tight')
plt.show()
