import numpy as np
import matplotlib.pyplot as plt
import torch

# Задание 2.4. Готовая реализация Adagrad из PyTorch

def f_np(x, y):
    return 1e-2 * (8*x**2 + 4*x*y + x + 4*y - 7)

def f_torch(point):
    x, y = point[0], point[1]
    return 1e-2 * (8*x**2 + 4*x*y + x + 4*y - 7)

saddle = np.array([-1.0, 15/4])
global_min = np.array([199/16, -50.0])
x0 = 20.0
y0 = saddle[1] + (np.sqrt(5) - 2) * (x0 - saddle[0])
start = np.array([x0, y0], dtype=float)

N = 100
lr = 3.5
eps = 1e-8

point = torch.tensor(start, dtype=torch.float64, requires_grad=True)
optimizer = torch.optim.Adagrad([point], lr=lr, eps=eps)
trajectory = [point.detach().numpy().copy()]

for _ in range(N):
    optimizer.zero_grad()
    loss = f_torch(point)
    loss.backward()
    optimizer.step()
    trajectory.append(point.detach().numpy().copy())

trajectory = np.array(trajectory)
final = trajectory[-1]

print('ЗАДАНИЕ 2.4 — PyTorch Adagrad')
print(f'Начальная точка: ({start[0]:.4f}, {start[1]:.4f})')
print(f'lr = {lr}, eps = {eps}, N = {N}')
print(f'Последняя точка: ({final[0]:.6f}, {final[1]:.6f})')
print(f'Расстояние до седловой точки: {np.linalg.norm(final - saddle):.6f}')

# Единственный график: траектория PyTorch Adagrad
x_min, x_max, y_min, y_max = -12, 22, -60, 12
xs = np.linspace(x_min, x_max, 500)
ys = np.linspace(y_min, y_max, 500)
X, Y = np.meshgrid(xs, ys)
Z = f_np(X, Y)

plt.figure(figsize=(10, 7))
cs = plt.contour(X, Y, Z, levels=40)
plt.clabel(cs, inline=True, fontsize=8)
plt.plot(trajectory[:, 0], trajectory[:, 1], marker='o', markersize=3, linewidth=1.2, label='PyTorch Adagrad')
plt.scatter(*start, marker='o', s=100, label='Начальное приближение')
plt.scatter(*saddle, marker='x', s=120, label='Седловая точка')
plt.scatter(*global_min, marker='*', s=180, label='Глобальный минимум')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xlabel('x')
plt.ylabel('y')
plt.title('PyTorch Adagrad: преодоление окрестности седловой точки')
plt.grid(True)
plt.legend()
plt.show()
