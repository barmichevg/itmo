import numpy as np
import matplotlib.pyplot as plt

# Задание 1. Аналитическое исследование функции

def f(x, y):
    return 1e-2 * (8*x**2 + 4*x*y + x + 4*y - 7)

x_min, x_max = -20, 20
y_min, y_max = -50, 50

saddle = np.array([-1.0, 15/4])
global_min = np.array([199/16, -50.0])

print('ЗАДАНИЕ 1')
print('df/dx = 10^-2(16x + 4y + 1)')
print('df/dy = 10^-2(4x + 4)')
print(f'Стационарная точка: ({saddle[0]}, {saddle[1]})')
print('H = [[0.16, 0.04], [0.04, 0]]')
print('det(H) = -0.0016 < 0, значит точка седловая')
print('Локальных экстремумов внутри области нет')
print(f'Глобальный минимум: ({global_min[0]:.4f}, {global_min[1]:.4f}), f_min = {f(*global_min):.7f}')
print()


xs = np.linspace(x_min, x_max, 400)
ys = np.linspace(y_min, y_max, 400)
X, Y = np.meshgrid(xs, ys)
Z = f(X, Y)

plt.figure(figsize=(10, 7))
cs = plt.contour(X, Y, Z, levels=40)
plt.clabel(cs, inline=True, fontsize=8)
plt.scatter(*saddle, marker='x', s=120, label='Седловая точка')
plt.scatter(*global_min, marker='*', s=180, label='Глобальный минимум')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Линии уровня функции варианта 11')
plt.grid(True)
plt.legend()
plt.show()
