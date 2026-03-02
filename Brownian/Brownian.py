import numpy as np
import matplotlib.pyplot as plt

L=100
a = 1.0
alpha = 1.5  # Lévy flight parameter

np.random.seed(2)
x0 = np.random.uniform(0, L)
y0 = np.random.uniform(0, L)
print(x0)
print(y0)

x_prey = np.random.uniform(0, L)
y_prey = np.random.uniform(0, L)
print(x_prey)
print(y_prey)

x, y = x0, y0
positions = [(x, y)]
distance = np.sqrt((x - x_prey)**2 + (y - y_prey)**2)

while distance > 1:
    x += np.random.uniform(-a, a)
   # * np.random.exponential(alpha)
    y += np.random.uniform(-a, a)
    x = np.clip(x, 0, L)
    y = np.clip(y, 0, L)
    positions.append((x, y))
    distance = np.sqrt((x - x_prey)**2 + (y - y_prey)**2)

positions = np.array(positions)
print(f"Number of steps: {len(positions) - 1}")

plt.figure(figsize=(8, 8))
plt.plot(positions[:, 0], positions[:, 1], 'b-', alpha=0.7, label='Brownian motion')
plt.plot(x0, y0, 'go', markersize=10, label='Start')
plt.plot(x_prey, y_prey, 'r*', markersize=15, label='Prey')
plt.xlim(0, L)
plt.ylim(0, L)
plt.legend()
plt.grid(True)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title(f'Brownian Motion - Number of steps: {len(positions) - 1}')
plt.savefig('Brownian.png', dpi=150, bbox_inches='tight')
plt.show()