import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return 1e-2 * (8*x**2 + 4*x*y + x + 4*y - 7)

def grad_f(x, y):
    return np.array([1e-2*(16*x + 4*y + 1), 1e-2*(4*x + 4)], dtype=float)

saddle = np.array([-1.0, 15/4])
global_min = np.array([199/16, -50.0])

x0 = 20.0
y0 = saddle[1] + (np.sqrt(5) - 2) * (x0 - saddle[0])
start = np.array([x0, y0], dtype=float)

def plot_trajectory(trajectory, title, view=(-20, 20, -50, 50)):
    x_min, x_max, y_min, y_max = view
    xs = np.linspace(x_min, x_max, 500)
    ys = np.linspace(y_min, y_max, 500)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)

    plt.figure(figsize=(10, 7))
    cs = plt.contour(X, Y, Z, levels=40)
    plt.clabel(cs, inline=True, fontsize=8)
    plt.plot(trajectory[:, 0], trajectory[:, 1], marker='o', markersize=3, linewidth=1.2, label='Траектория')
    plt.scatter(*start, marker='o', s=100, label='Начальное приближение')
    plt.scatter(*saddle, marker='x', s=120, label='Седловая точка')
    plt.scatter(*global_min, marker='*', s=180, label='Глобальный минимум')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

# Задание 2.3. Подбор гиперпараметров

def adagrad(start, alpha, eps, n_iter):
    point = start.copy()
    G = np.zeros_like(point)
    trajectory = [point.copy()]
    for _ in range(n_iter):
        grad = grad_f(*point)
        G += grad**2
        point = point - alpha * grad / (np.sqrt(G) + eps)
        trajectory.append(point.copy())
    return np.array(trajectory)

N = 100
eps = 1e-8
traj_zigzag = adagrad(start, 30.0, eps, N)
traj_smooth = adagrad(start, 3.5, eps, N)

print('ЗАДАНИЕ 2.3 — подбор гиперпараметров')
print('Область отображения: x in [-12, 22], y in [-60, 12]')
print('1) alpha = 30, eps = 1e-8 — пилообразная траектория')
print('2) alpha = 3.5, eps = 1e-8 — более чёткое движение')

x_min, x_max, y_min, y_max = -12, 22, -60, 12
xs = np.linspace(x_min, x_max, 500)
ys = np.linspace(y_min, y_max, 500)
X, Y = np.meshgrid(xs, ys)
Z = f(X, Y)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
for ax, trajectory, title in [
    (axes[0], traj_zigzag, 'Пилообразная траектория\nalpha=30, eps=1e-8'),
    (axes[1], traj_smooth, 'Более чёткое движение\nalpha=3.5, eps=1e-8'),
]:
    cs = ax.contour(X, Y, Z, levels=40)
    ax.clabel(cs, inline=True, fontsize=7)
    ax.plot(trajectory[:, 0], trajectory[:, 1], marker='o', markersize=3, linewidth=1.2)
    ax.scatter(*start, marker='o', s=90, label='Начальное приближение')
    ax.scatter(*saddle, marker='x', s=110, label='Седловая точка')
    ax.scatter(*global_min, marker='*', s=150, label='Глобальный минимум')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)
    ax.grid(True)
    ax.legend()
plt.tight_layout()
plt.show()
