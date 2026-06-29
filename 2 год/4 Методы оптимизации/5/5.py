import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = np.array([
    [0.85, 1.12, 0.73],
    [1.83, 2.20, 3.65],
    [2.91, 3.12, 4.86],
    [3.93, 3.92, 2.00],
    [4.86, 4.94, 0.32]
], dtype=float)

X = data[:, 0]
Y = data[:, 1]
Z = data[:, 2]
points = data[:, :2]

# RBF-сеть с 2 скрытыми нейронами: z_hat = w0 + w1*phi1 + w2*phi2
def kmeans_2d(points, k=2, seed=42, max_iter=100, tol=1e-10):
    rng = np.random.default_rng(seed)

    # Случайно выбираем начальные центры
    indices = rng.choice(len(points), size=k, replace=False)
    centers = points[indices].copy()

    history = [centers.copy()]

    for _ in range(max_iter):
        # расстояния от каждой точки до каждого центра
        d2 = ((points[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = np.argmin(d2, axis=1)

        # Пересчитываем центры как средние по кластерам
        new_centers = centers.copy()
        for j in range(k):
            cluster_points = points[labels == j]
            if len(cluster_points) > 0:
                new_centers[j] = cluster_points.mean(axis=0)

        history.append(new_centers.copy())

        # Остановка, если центры почти не меняются
        if np.linalg.norm(new_centers - centers) < tol:
            centers = new_centers
            break

        centers = new_centers

    return centers, labels, history


def rbf_features(X, Y, c1x, c1y, c2x, c2y, sigma1, sigma2):
    # Квадраты расстояний до 2 центров
    r1_sq = (X - c1x) ** 2 + (Y - c1y) ** 2
    r2_sq = (X - c2x) ** 2 + (Y - c2y) ** 2

    # Значения двух радиально-базисных функций
    phi1 = np.exp(-r1_sq / (2.0 * sigma1 ** 2))
    phi2 = np.exp(-r2_sq / (2.0 * sigma2 ** 2))
    return phi1, phi2, r1_sq, r2_sq


def predict_rbf(X, Y, params):
    # Считаем предсказание сети по текущим параметрам
    w0, w1, w2, c1x, c1y, c2x, c2y, sigma1, sigma2 = params
    phi1, phi2, _, _ = rbf_features(X, Y, c1x, c1y, c2x, c2y, sigma1, sigma2)
    return w0 + w1 * phi1 + w2 * phi2


# Функция потерь MSE
def mse_loss(y_pred, y_true):
    
    return 0.5 * np.mean((y_pred - y_true) ** 2)


def compute_gradients(X, Y, Z, params):
    # Вычисляем градиенты loss по всем параметрам сети
    w0, w1, w2, c1x, c1y, c2x, c2y, sigma1, sigma2 = params

    phi1, phi2, r1_sq, r2_sq = rbf_features(X, Y, c1x, c1y, c2x, c2y, sigma1, sigma2)
    y_pred = w0 + w1 * phi1 + w2 * phi2
    errors = y_pred - Z

    # Производные по весам
    dw0 = np.mean(errors)
    dw1 = np.mean(errors * phi1)
    dw2 = np.mean(errors * phi2)

    # Производные по координатам центров
    dc1x = np.mean(errors * w1 * phi1 * (X - c1x) / (sigma1 ** 2))
    dc1y = np.mean(errors * w1 * phi1 * (Y - c1y) / (sigma1 ** 2))
    dc2x = np.mean(errors * w2 * phi2 * (X - c2x) / (sigma2 ** 2))
    dc2y = np.mean(errors * w2 * phi2 * (Y - c2y) / (sigma2 ** 2))

    # Производные по ширинам sigma
    dsigma1 = np.mean(errors * w1 * phi1 * r1_sq / (sigma1 ** 3))
    dsigma2 = np.mean(errors * w2 * phi2 * r2_sq / (sigma2 ** 3))

    grads = np.array([dw0, dw1, dw2, dc1x, dc1y, dc2x, dc2y, dsigma1, dsigma2], dtype=float)
    return grads, y_pred


# инициализация сети
# ищем начальные центры через K-Means
centers, labels, km_history = kmeans_2d(points, k=2, seed=42)

# упорядочиваем центры для удобства
centers = centers[np.argsort(centers[:, 0])]
(c1x0, c1y0), (c2x0, c2y0) = centers

dist_centers = np.linalg.norm(centers[1] - centers[0])
sigma1_0 = max(dist_centers / 2.0, 1e-3)
sigma2_0 = max(dist_centers / 2.0, 1e-3)

# начальные веса
w0_0 = 0.0
w1_0 = 0.1
w2_0 = -0.1

# Общий вектор параметров
params = np.array([w0_0, w1_0, w2_0, c1x0, c1y0, c2x0, c2y0, sigma1_0, sigma2_0], dtype=float)

print("=" * 70)
print("ИНИЦИАЛИЗАЦИЯ")
print("=" * 70)
print(f"Центр 1: ({c1x0:.6f}, {c1y0:.6f})")
print(f"Центр 2: ({c2x0:.6f}, {c2y0:.6f})")
print(f"Начальные sigma: sigma1 = {sigma1_0:.6f}, sigma2 = {sigma2_0:.6f}")
print(f"Начальные веса: w0 = {w0_0:.6f}, w1 = {w1_0:.6f}, w2 = {w2_0:.6f}")

# обучение градиентным спуском
learning_rate = 0.2
n_epochs = 1000
min_sigma = 1e-3
loss_history = []

for epoch in range(n_epochs):
    # Считаем градиенты и предсказания
    grads, y_pred = compute_gradients(X, Y, Z, params)

    # Считаем loss на текущей итерации
    loss = mse_loss(y_pred, Z)
    loss_history.append(loss)

    # Выводим loss
    if epoch < 20 or (epoch + 1) % 100 == 0:
        print(f"Итерация {epoch + 1:4d}: loss = {loss:.12e}")

    # Ограничиваем слишком большой градиент
    grad_norm = np.linalg.norm(grads)
    if grad_norm > 10.0:
        grads = grads * (10.0 / grad_norm)

    # Обновляем параметры по формуле градиентного спуска
    params -= learning_rate * grads

    # Не даём sigma стать неположительными
    params[7] = max(params[7], min_sigma)
    params[8] = max(params[8], min_sigma)


w0, w1, w2, c1x, c1y, c2x, c2y, sigma1, sigma2 = params
predictions = predict_rbf(X, Y, params)
residuals = Z - predictions
final_loss = mse_loss(predictions, Z)

print("\n" + "=" * 70)
print("ИТОГОВАЯ МОДЕЛЬ")
print("=" * 70)
print(f"w0 = {w0:.12f}")
print(f"w1 = {w1:.12f}")
print(f"w2 = {w2:.12f}")
print(f"c1 = ({c1x:.12f}, {c1y:.12f})")
print(f"c2 = ({c2x:.12f}, {c2y:.12f})")
print(f"sigma1 = {sigma1:.12f}")
print(f"sigma2 = {sigma2:.12f}")
print(f"\nФинальный loss = {final_loss:.16e}")

# Невязки по точкам
print("\nНевязки по точкам:")
for i in range(len(X)):
    print(
        f"Точка {i + 1}: "
        f"z = {Z[i]:.6f}, "
        f"z_hat = {predictions[i]:.6f}, "
        f"невязка = {residuals[i]:.6e}"
    )

# ---------- ГРАФИК НЕВЯЗОК ----------

plt.figure(figsize=(7, 4))
plt.bar(range(1, len(residuals) + 1), residuals)
plt.axhline(0, color='black', linewidth=1)
plt.xlabel("Номер точки")
plt.ylabel("Невязка")
plt.title("График невязок для RBF-сети")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Итоговая аналитическая формула
print("\nАналитический вид модели:")
print("z_RBF(x, y) = "
      f"{w1:.6f} * exp(-((x - {c1x:.6f})^2 + (y - {c1y:.6f})^2) / (2 * {sigma1:.6f}^2)) + "
      f"{w2:.6f} * exp(-((x - {c2x:.6f})^2 + (y - {c2y:.6f})^2) / (2 * {sigma2:.6f}^2)) + "
      f"{w0:.6f}")

# ---------- ВИЗУАЛИЗАЦИЯ ----------

# Строим сетку для поверхности
x_grid = np.linspace(0, 6, 120)
y_grid = np.linspace(0, 6, 120)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
Z_grid = predict_rbf(X_grid, Y_grid, params)

fig = plt.figure(figsize=(18, 5))

# Кривая обучения: loss от номера итерации
ax1 = fig.add_subplot(131)
ax1.plot(loss_history, color='blue', linewidth=2)
ax1.set_yscale('log')
ax1.set_xlabel("Номер итерации")
ax1.set_ylabel("Loss (MSE)")
ax1.set_title("Кривая обучения")
ax1.grid(True, alpha=0.3)

# 3D-поверхность модели
ax2 = fig.add_subplot(132, projection='3d')
ax2.plot_surface(X_grid, Y_grid, Z_grid, cmap='viridis', alpha=0.85)
ax2.scatter(X, Y, Z, c='red', s=60, label='Точки данных')
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")
ax2.set_title("Модельная поверхность RBF")
ax2.legend()

# Линии уровня модели + исходные точки
ax3 = fig.add_subplot(133)
contour = ax3.contourf(X_grid, Y_grid, Z_grid, levels=30, cmap='viridis', alpha=0.9)
ax3.contour(X_grid, Y_grid, Z_grid, levels=12, colors='white', linewidths=0.6, alpha=0.5)
ax3.scatter(X, Y, c=Z, s=120, edgecolors='black', cmap='viridis', label='Точки данных')
ax3.set_xlabel("X")
ax3.set_ylabel("Y")
ax3.set_title("Линии уровня и точки данных")
ax3.grid(True, alpha=0.3)
ax3.legend()
plt.colorbar(contour, ax=ax3, label="Z")

plt.tight_layout()
plt.show()