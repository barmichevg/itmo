import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

data = np.array([
    [0.85, 1.12, 0.73],
    [1.83, 2.20, 3.65],
    [2.91, 3.12, 4.86],
    [3.93, 3.92, 2.00],
    [4.86, 4.94, 0.32]
])

X = data[:, 0]
Y = data[:, 1]
Z = data[:, 2]

print("Исходные данные:")
for i in range(len(X)):
    print(f"  Точка {i}: x={X[i]:.2f}, y={Y[i]:.2f}, z={Z[i]:.2f}")


def paraboloid_model(x, y, x0, y0, z0, a, b, c):
    dx = x - x0
    dy = y - y0
    return a * dx**2 + b * dy**2 + c * dx * dy + z0


def loss_function(params):
    x0, y0, z0, a, b, c = params

    predictions = paraboloid_model(X, Y, x0, y0, z0, a, b, c)
    errors = Z - predictions
    mse = 0.5 * np.mean(errors**2)

    penalty = 0.0

    if a >= 0 or b >= 0:
        penalty += 1e6

    ellipticity = 4 * a * b - c**2
    if ellipticity <= 1e-10:
        penalty += 1e6 * (1 + abs(ellipticity))

    return mse + penalty

loss_history = []

def logger(xk):
    current_loss = loss_function(xk)
    loss_history.append(current_loss)
    print(f"Итерация {len(loss_history):3d}: loss = {current_loss:.12e}")


max_idx = np.argmax(Z)

x0_start = min(6.0, X[max_idx] + 0.3)
y0_start = min(6.0, Y[max_idx] + 0.4)
z0_start = Z[max_idx] + 1.0

a_start = -0.5
b_start = -0.5
c_start = 0.0

params_start = [x0_start, y0_start, z0_start, a_start, b_start, c_start]

print("\nНачальное приближение:")
print(f"  x0 = {x0_start:.4f}")
print(f"  y0 = {y0_start:.4f}")
print(f"  z0 = {z0_start:.4f}")
print(f"  a  = {a_start:.4f}")
print(f"  b  = {b_start:.4f}")
print(f"  c  = {c_start:.4f}")

loss_history.append(loss_function(params_start))

bounds = [
    (0.0, 6.0),
    (0.0, 6.0),
    (-10.0, 10.0),
    (-20.0, -1e-6),
    (-20.0, -1e-6),
    (-20.0, 20.0)
]

print("\nЗапускаем оптимизацию L-BFGS-B...")
result = minimize(
    loss_function,
    params_start,
    method='L-BFGS-B',
    bounds=bounds,
    callback=logger,
    options={'maxiter': 500}
)

x0_opt, y0_opt, z0_opt, a_opt, b_opt, c_opt = result.x

predictions = paraboloid_model(X, Y, x0_opt, y0_opt, z0_opt, a_opt, b_opt, c_opt)
residuals = Z - predictions
mse_final = 0.5 * np.mean(residuals**2)
ellipticity_final = 4 * a_opt * b_opt - c_opt**2

print("\n" + "=" * 60)
print("РЕЗУЛЬТАТЫ АППРОКСИМАЦИИ ЭЛЛИПТИЧЕСКИМ ПАРАБОЛОИДОМ")
print("=" * 60)

print(f"\nx0 = {x0_opt:.6f}")
print(f"y0 = {y0_opt:.6f}")
print(f"z0 = {z0_opt:.6f}")
print(f"a  = {a_opt:.6f}")
print(f"b  = {b_opt:.6f}")
print(f"c  = {c_opt:.6f}")

print(f"\nФинальная MSE = {mse_final:.12f}")
print(f"Проверка эллиптичности: 4ab - c^2 = {ellipticity_final:.12f}")
print(f"Статус оптимизации: {result.message}")

print("\nНевязки по точкам:")
for i in range(len(X)):
    print(
        f"  Точка {i}: "
        f"z_ист={Z[i]:.6f}, "
        f"z_мод={predictions[i]:.6f}, "
        f"невязка={residuals[i]:.6e}"
    )
plt.figure(figsize=(7, 4))
plt.bar(range(1, len(residuals) + 1), residuals)
plt.axhline(0, color='black', linewidth=1)
plt.xlabel("Номер точки")
plt.ylabel("Невязка")
plt.title("График невязок для параболоида")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\nАналитический вид модели:")
print(
    f"z(x, y) = {a_opt:.6f}(x - {x0_opt:.6f})^2 "
    f"+ {b_opt:.6f}(y - {y0_opt:.6f})^2 "
    f"+ {c_opt:.6f}(x - {x0_opt:.6f})(y - {y0_opt:.6f}) "
    f"+ {z0_opt:.6f}"
)

x_grid = np.linspace(0, 6, 120)
y_grid = np.linspace(0, 6, 120)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
Z_grid = paraboloid_model(X_grid, Y_grid, x0_opt, y0_opt, z0_opt, a_opt, b_opt, c_opt)

# Графики
fig = plt.figure(figsize=(18, 5))

# Кривая обучения
ax1 = fig.add_subplot(131)
ax1.plot(range(len(loss_history)), loss_history, marker='o', linewidth=2)
ax1.set_yscale('log')
ax1.set_xlabel('Номер итерации')
ax1.set_ylabel('Loss (MSE + penalty)')
ax1.set_title('Кривая обучения')
ax1.grid(True, alpha=0.3)

# 3D поверхность
ax2 = fig.add_subplot(132, projection='3d')
ax2.plot_surface(X_grid, Y_grid, Z_grid, cmap='viridis', alpha=0.85)
ax2.scatter(X, Y, Z, c='red', s=60, label='Data points')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Модельная поверхность')
ax2.legend()

# Линии уровня
ax3 = fig.add_subplot(133)
contour = ax3.contourf(X_grid, Y_grid, Z_grid, levels=30, cmap='viridis', alpha=0.9)
ax3.contour(X_grid, Y_grid, Z_grid, levels=12, colors='white', linewidths=0.7, alpha=0.5)
scatter = ax3.scatter(X, Y, c=Z, s=120, edgecolors='black', cmap='viridis', label='Точки данных')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_title('Линии уровня и точки данных')
ax3.grid(True, alpha=0.3)
ax3.legend()
plt.colorbar(contour, ax=ax3, label='Z')
plt.tight_layout()
plt.show()