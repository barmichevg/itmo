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

# Задание 2.1. Обычный градиентный спуск

def gradient_descent(start, alpha, eps_grad, eps_f, max_iter):
    point = start.copy()
    trajectory = [point.copy()]
    for k in range(1, max_iter + 1):
        new_point = point - alpha * grad_f(*point)
        grad_norm = np.linalg.norm(grad_f(*new_point))
        f_diff = abs(f(*new_point) - f(*point))
        trajectory.append(new_point.copy())
        point = new_point
        if grad_norm < eps_grad and f_diff < eps_f:
            return np.array(trajectory), k
    return np.array(trajectory), max_iter

alpha = 0.5
eps_grad = 5.5e-4
eps_f = 1.7e-7
trajectory, n_iter = gradient_descent(start, alpha, eps_grad, eps_f, 1000)
final = trajectory[-1]

print('ЗАДАНИЕ 2.1 — обычный градиентный спуск')
print(f'Начальная точка: ({start[0]:.4f}, {start[1]:.4f})')
print(f'alpha = {alpha}, eps_grad = {eps_grad}, eps_f = {eps_f}')
print(f'Количество итераций: {n_iter}')
print(f'Последняя точка: ({final[0]:.6f}, {final[1]:.6f})')
print(f'Расстояние до седловой точки: {np.linalg.norm(final - saddle):.8f}')

plot_trajectory(trajectory, 'Обычный градиентный спуск: сходимость к седловой точке')
