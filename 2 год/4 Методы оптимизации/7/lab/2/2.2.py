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

# Задание 2.2. Собственная реализация Adagrad

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

alpha = 3.5
eps = 1e-8
N = 100
trajectory = adagrad(start, alpha, eps, N)
final = trajectory[-1]
distances = np.linalg.norm(trajectory - saddle, axis=1)
closest_iter = np.argmin(distances)

print('ЗАДАНИЕ 2.2 — собственная реализация Adagrad')
print(f'Начальная точка: ({start[0]:.4f}, {start[1]:.4f})')
print(f'alpha = {alpha}, eps = {eps}, N = {N}')
print(f'Последняя точка: ({final[0]:.6f}, {final[1]:.6f})')
print(f'Ближе всего к седловой точке: итерация {closest_iter}, расстояние {distances[closest_iter]:.6f}')

plot_trajectory(trajectory, 'Собственный Adagrad: преодоление окрестности седловой точки')
