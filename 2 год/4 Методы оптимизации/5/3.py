import numpy as np

data = np.array([
    [0.85, 1.12, 0.73],
    [1.83, 2.20, 3.65],
    [2.91, 3.12, 4.86],
    [3.93, 3.92, 2.00],
    [4.86, 4.94, 0.32]
])

Z = data[:, 2]

# Лучшая константа для MSE
const_mse = np.mean(Z)

# Лучшая константа для MAE
const_mae = np.median(Z)

# Значения ошибок
mse_value = 0.5 * np.mean((Z - const_mse) ** 2)
mae_value = np.mean(np.abs(Z - const_mae))

print("Значения z:")
print(Z)

print("\nЛучшая константная модель в смысле минимизации MSE:")
print(f"z(x, y) = {const_mse:.3f}")
print(f"MSE = {mse_value:.6f}")

print("\nЛучшая константная модель в смысле минимизации MAE:")
print(f"z(x, y) = {const_mae:.3f}")
print(f"MAE = {mae_value:.6f}")