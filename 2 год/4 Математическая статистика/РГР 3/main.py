import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "data.csv"
df = pd.read_csv(file_path)

x = df["x"].values
y = df["y"].values
n = len(df)

# Линейная модель
b_lin, a_lin = np.polyfit(x, y, 1)
y_hat_lin = a_lin + b_lin * x

# Квадратичная модель
c_quad, b_quad, a_quad = np.polyfit(x, y, 2)
y_hat_quad = a_quad + b_quad * x + c_quad * x**2

# Степенная модель
ln_x = np.log(x)
ln_y = np.log(y)

b_pow, ln_a_pow = np.polyfit(ln_x, ln_y, 1)
a_pow = np.exp(ln_a_pow)
y_hat_pow = a_pow * x**b_pow


# Метрики качества
def regression_metrics(y_true, y_pred):
    residuals = y_true - y_pred
    rss = np.sum(residuals**2)
    tss = np.sum((y_true - np.mean(y_true))**2)
    r2 = 1 - rss / tss
    rmse = np.sqrt(np.mean(residuals**2))
    mean_approx_error = np.mean(np.abs(residuals / y_true)) * 100

    return {
        "RSS": rss,
        "R2": r2,
        "RMSE": rmse,
        "A": mean_approx_error
    }

metrics_lin = regression_metrics(y, y_hat_lin)
metrics_quad = regression_metrics(y, y_hat_quad)
metrics_pow = regression_metrics(y, y_hat_pow)


# Вывод по моделям
print("1) Линейная модель")
print(f"a = {a_lin:.6f}")
print(f"b = {b_lin:.6f}")
print(f"Итоговое уравнение: y_hat = {a_lin:.6f} + {b_lin:.6f} * x")
print(f"RSS = {metrics_lin['RSS']:.6f}")
print(f"R^2 = {metrics_lin['R2']:.6f}")
print(f"RMSE = {metrics_lin['RMSE']:.6f}")
print(f"A = {metrics_lin['A']:.6f}")

print("\n2) Квадратичная модель")
print(f"a = {a_quad:.6f}")
print(f"b = {b_quad:.6f}")
print(f"c = {c_quad:.10f}")
print(f"Итоговое уравнение: y_hat = {a_quad:.6f} + {b_quad:.6f} * x + {c_quad:.10f} * x^2")
print(f"RSS = {metrics_quad['RSS']:.6f}")
print(f"R^2 = {metrics_quad['R2']:.6f}")
print(f"RMSE = {metrics_quad['RMSE']:.6f}")
print(f"A = {metrics_quad['A']:.6f}")

print("\n3) Степенная модель")
print("Линеаризация: ln(y) = ln(a) + b * ln(x)")
print(f"ln(a) = {ln_a_pow:.6f}")
print(f"a = {a_pow:.6f}")
print(f"b = {b_pow:.6f}")
print(f"Итоговое уравнение: y_hat = {a_pow:.6f} * x^{b_pow:.6f}")
print(f"RSS = {metrics_pow['RSS']:.6f}")
print(f"R^2 = {metrics_pow['R2']:.6f}")
print(f"RMSE = {metrics_pow['RMSE']:.6f}")
print(f"A = {metrics_pow['A']:.6f}")


# Вычисление S_xx
x_mean = np.mean(x)
S_xx = np.sum((x - x_mean)**2)

print(f"\nСреднее x̄ = {x_mean:.6f}")
print(f"S_xx = Σ(x_i - x̄)^2 = {S_xx:.6f}")

# Таблица сравнения качества моделей
metrics = pd.DataFrame({
    "Линейная модель": {"RSS": metrics_lin["RSS"], "R2": metrics_lin["R2"], "RMSE": metrics_lin["RMSE"], "Mean approximation error, %": metrics_lin["A"]},
    "Квадратичная модель": {"RSS": metrics_quad["RSS"], "R2": metrics_quad["R2"], "RMSE": metrics_quad["RMSE"], "Mean approximation error, %": metrics_quad["A"]},
    "Степенная модель": {"RSS": metrics_pow["RSS"], "R2": metrics_pow["R2"], "RMSE": metrics_pow["RMSE"], "Mean approximation error, %": metrics_pow["A"]}
}).T

print("\nСравнение качества трёх моделей")
print(metrics.to_string(float_format=lambda value: f"{value:.6f}"))


# Таблица остатков
df["residual_linear"] = y - y_hat_lin
df["residual_quadratic"] = y - y_hat_quad
df["residual_power"] = y - y_hat_pow

print("\nТаблица остатков:")
print(df[["i", "x", "y", "residual_linear", "residual_quadratic", "residual_power"]].to_string(index=False))


# График сравнения моделей
x_grid = np.linspace(x.min(), x.max(), 500)
y_grid_lin = a_lin + b_lin * x_grid
y_grid_quad = a_quad + b_quad * x_grid + c_quad * x_grid**2
y_grid_pow = a_pow * x_grid**b_pow

plt.figure(figsize=(9, 6))
plt.scatter(x, y, label="Исходные данные")
plt.plot(x_grid, y_grid_lin, label="Линейная модель")
plt.plot(x_grid, y_grid_quad, label="Квадратичная модель")
plt.plot(x_grid, y_grid_pow, label="Степенная модель")
plt.xlabel("Скорость чтения x, МБ/с")
plt.ylabel("Скорость записи y, МБ/с")
plt.title("Сравнение регрессионных моделей")
plt.grid(True)
plt.legend()
plt.show()


# Графики остатков
plt.figure(figsize=(8, 5))
plt.scatter(x, df["residual_linear"])
plt.axhline(0, linestyle="--")
plt.xlabel("Скорость чтения x, МБ/с")
plt.ylabel("Остатки e_i, МБ/с")
plt.title("График остатков линейной модели")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(x, df["residual_quadratic"])
plt.axhline(0, linestyle="--")
plt.xlabel("Скорость чтения x, МБ/с")
plt.ylabel("Остатки e_i, МБ/с")
plt.title("График остатков квадратичной модели")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(x, df["residual_power"])
plt.axhline(0, linestyle="--")
plt.xlabel("Скорость чтения x, МБ/с")
plt.ylabel("Остатки e_i, МБ/с")
plt.title("График остатков степенной модели")
plt.grid(True)
plt.show()
