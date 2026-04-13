import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

L=20
N_pasos=5000
alpha_0=3.0
alpha_f=4.0
delta_alpha=0.05
l_min=1.0 #necesario para normalizar la power law
pasos=0

promedios = []
steps = []
alphas = []
error= []

np.random.seed(22)

#----------- FUNCION LEVY (POWER LAW) -----------
def power_law_step(alpha, l_min):
    u=np.random.uniform(0, 1)
    return l_min*(1-u)**(-1/(alpha-1))

for alpha in np.arange(alpha_0,alpha_f,delta_alpha):
    
    for i in range(N_pasos):
        pasos=0
        x0 = np.random.uniform(0, L)
        y0 = np.random.uniform(0, L)
        z0 = np.random.uniform(0, L)


        x_prey = np.random.uniform(0, L)
        y_prey = np.random.uniform(0, L)
        z_prey = np.random.uniform(0, L)


        x, y, z = x0, y0,z0

        distance_square = (x - x_prey)**2 + (y - y_prey)**2 + (z - z_prey)**2

        inv_exp = -1/(alpha - 1)   # calcular fuera del while

        while distance_square > 1:
        
            # Dirección aleatoria uniforme
            dx, dy, dz = np.random.normal(size=3)
            norm = np.sqrt(dx*dx + dy*dy + dz*dz)
            dx /= norm
            dy /= norm
            dz /= norm

            # Paso power-law (inline)
            u = np.random.rand()
            step_length = l_min * (1 - u)**inv_exp

            x += step_length * dx
            y += step_length * dy
            z += step_length * dz

            # Clip manual rápido
            if x < 0: x = 0
            elif x > L: x = L

            if y < 0: y = 0
            elif y > L: y = L

            if z < 0: z = 0
            elif z > L: z = L

            dxp = x - x_prey
            dyp = y - y_prey
            dzp = z - z_prey
            distance_square = dxp*dxp + dyp*dyp + dzp*dzp

            pasos += 1
        
        steps.append(pasos)
        if i%1000==0:
            print(f"Paso {i} - Distance to prey: {np.sqrt(distance_square):.2f} - Steps so far: {pasos}")
    print(f"Alpha {alpha}")
 
    promedio=(np.mean(steps))
    std = np.std(steps)
    
    alphas.append(alpha)
    promedios.append(promedio)
    error.append(std/np.sqrt(N_pasos))  # Error estándar de la media
    steps.clear()  # Limpiar para la siguiente alpha

# Save results to file
with open(f'Results/Levy/Data/3D/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.txt', 'w') as f:
    f.write("Alpha\tAverage_Steps\tStd_Dev\n")
    for alpha, promedio, std in zip(alphas, promedios, error):
        f.write(f"{alpha:.2f}\t{promedio:.2f}\t{std:.2f}\n")

#AQUÍ HACE UNO FUERA DE SIMULACIÓN PARA PLOTEARLO
#==========================================================================================
x, y, z = x0, y0, z0
distance_square = (x - x_prey)**2 + (y - y_prey)**2 + (z - z_prey)**2

positions = [(x, y, z)]

while distance_square > 1:

    dx, dy, dz = np.random.normal(size=3)
    norm = np.sqrt(dx*dx + dy*dy + dz*dz)

    dx /= norm
    dy /= norm
    dz /= norm
    step_length = power_law_step(alpha, l_min)

    x += step_length * dx
    y += step_length * dy
    z += step_length * dz

    x = np.clip(x, 0, L)
    y = np.clip(y, 0, L)
    z = np.clip(z, 0, L)

    distance_square = (x - x_prey)**2 + (y - y_prey)**2 + (z - z_prey)**2
    positions.append((x, y, z))

positions = np.array(positions)
print(f"Number of steps: {len(positions) - 1}")


fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', alpha=0.7, label='Lèvy flight')
ax.scatter(x0, y0, z0, c='g', s=60, label='Start')
ax.scatter(x_prey, y_prey, z_prey, c='r', s=100, marker='*', label='Prey')
ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_zlim(0, L)
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.legend()
ax.grid(True)
ax.set_title(f"Lèvy Flight 3D - Number of steps: {len(positions) - 1}")
plt.savefig(f'Levy/Levy3D.png', dpi=150, bbox_inches='tight')
plt.show()
#===========================================================================================================

plt.figure(figsize=(8, 6))
plt.errorbar(alphas, promedios, yerr=error, fmt='ro-', alpha=0.7, capsize=5, ecolor='black')
plt.xlabel('Alpha')
plt.ylabel('Average Number of Steps to Reach Prey')
plt.title(f'L = {L},N_pasos = {N_pasos}, alpha_range = {alpha_0}-{alpha_f}, Delta_alpha = {delta_alpha}')
plt.grid(True)
plt.show()

