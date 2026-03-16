import numpy as np
import matplotlib.pyplot as plt

L=100
N_pasos=100000
alpha_0=2.2
alpha_f=2.4
delta_alpha=0.01
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


        x_prey = np.random.uniform(0, L)
        y_prey = np.random.uniform(0, L)


        x, y = x0, y0

        distance_square = (x - x_prey)**2 + (y - y_prey)**2

        inv_exp = -1/(alpha - 1)   # calcular fuera del while

        while distance_square > 1:
        
            # Dirección aleatoria uniforme
            dx, dy = np.random.normal(size=2)
            norm = (dx*dx + dy*dy)**0.5
            dx /= norm
            dy /= norm

            # Paso power-law (inline)
            u = np.random.rand()
            step_length = l_min * (1 - u)**inv_exp

            x += step_length * dx
            y += step_length * dy

            # Clip manual rápido
            if x < 0: x = 0
            elif x > L: x = L

            if y < 0: y = 0
            elif y > L: y = L

            dxp = x - x_prey
            dyp = y - y_prey
            distance_square = dxp*dxp + dyp*dyp

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
with open(f'Results/Levy/Data/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.txt', 'w') as f:
    f.write("Alpha\tAverage_Steps\tStd_Dev\n")
    for alpha, promedio, std in zip(alphas, promedios, error):
        f.write(f"{alpha:.2f}\t{promedio:.2f}\t{std:.2f}\n")

#AQUÍ HACE UNO FUERA DE SIMULACIÓN PARA PLOTEARLO
#==========================================================================================
x, y = x0, y0
distance_square = (x - x_prey)**2 + (y - y_prey)**2

positions = [(x, y)]

while distance_square > 1:
    angle = np.random.uniform(0, 2*np.pi)
    step_length = power_law_step(alpha, l_min)

    x += step_length * np.cos(angle)
    y += step_length * np.sin(angle)

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
plt.errorbar(alphas, promedios, yerr=error, fmt='ro-', alpha=0.7, capsize=5, ecolor='black')
plt.xlabel('Alpha')
plt.ylabel('Average Number of Steps to Reach Prey')
plt.title(f'L = {L},N_pasos = {N_pasos}, alpha_range = {alpha_0}-{alpha_f}, Delta_alpha = {delta_alpha}')
plt.grid(True)
plt.show()

