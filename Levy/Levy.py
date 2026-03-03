import numpy as np
import matplotlib.pyplot as plt

L=50
N_pasos=10000
alpha_0=1.8
alpha_f=2.5
delta_alpha=0.05
l_min=1.0 #necesario para normalizar la power law
suma=0

promedios = []
alphas = []


np.random.seed(832)

#----------- FUNCION LEVY (POWER LAW) -----------
def power_law_step(alpha, l_min):
    u=np.random.uniform(0, 1)
    return l_min*(1-u)**(-1/(alpha-1))

for alpha in np.arange(alpha_0,alpha_f,delta_alpha):
    suma=0
    for i in range(N_pasos):

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

            suma += 1
        if i%100==0:
            print(f"Paso {i} - Distance to prey: {np.sqrt(distance_square):.2f} - Steps so far: {suma}")
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
plt.plot(alphas, promedios, 'ro-', alpha=0.7)  
plt.xlabel('Alpha')
plt.ylabel('Average Number of Steps to Reach Prey')
plt.title(f'L = {L},N_pasos = {N_pasos}, alpha_range = {alpha_0}-{alpha_f}, Delta_alpha = {delta_alpha}')
plt.grid(True)
plt.savefig(f"Results/Levy/L{L}_Npasos{N_pasos}_alpharange{alpha_0}-{alpha_f}_deltaalpha{delta_alpha}.png", dpi=150, bbox_inches='tight')
plt.show()

