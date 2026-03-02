import numpy as np
import matplotlib.pyplot as plt

L=10
N_pasos=10
alpha_0=1.5
alpha_f=3
delta_alpha=0.2
suma=0

promedios = []
alphas = []


np.random.seed(22)

for alpha in np.arange(alpha_0,alpha_f,delta_alpha):
    suma=0
    for i in range(N_pasos):

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
    print(f"Alpha {alpha}")
 
    promedio=(suma-1)/N_pasos
    alphas.append(alpha)
    promedios.append(promedio)

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
plt.title(f"Lèvy Flight - Number of steps: {len(positions) - 1}")
plt.savefig(f'Levy/Levy.png', dpi=150, bbox_inches='tight')
plt.show()
#===========================================================================================================

plt.figure(figsize=(8, 6))
plt.plot(alphas, promedios, 'ro-', alpha=0.7)  
plt.xlabel('Alpha')
plt.ylabel('Average Number of Steps to Reach Prey')
plt.title(f'L = {L},N_pasos = {N_pasos}, alpha_range = {alpha_0}-{alpha_f}, Delta_alpha = {delta_alpha}')
plt.grid(True)
plt.savefig(f"Results/Levy/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.png", dpi=150, bbox_inches='tight')
plt.show()
