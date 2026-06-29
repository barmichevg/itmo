import numpy as np

data = np.array([
    [0.85, 1.12, 0.73],
    [1.83, 2.20, 3.65],
    [2.91, 3.12, 4.86],
    [3.93, 3.92, 2.00],
    [4.86, 4.94, 0.32]
], dtype=float)

points = data[:, :2]
Z = data[:, 2]
X = points[:, 0]
Y = points[:, 1]
m = len(points)

def dist2(p, c):
    return np.sum((p - c) ** 2)

def print_points():
    print("Исходные данные:")
    for i, (x, y, z) in enumerate(data, start=1):
        print(f"{i}: x={x:.2f}, y={y:.2f}, z={z:.2f}")
    print()

def kmeans_step(points, centers):
    clusters = {0: [], 1: []}

    print("Таблица расстояний до центров:")
    for i, p in enumerate(points, start=1):
        d0 = dist2(p, centers[0])
        d1 = dist2(p, centers[1])

        cluster_id = 0 if d0 <= d1 else 1
        clusters[cluster_id].append(p)

        print(
            f"Точка {i}: "
            f"d1^2 = {d0:.4f}, "
            f"d2^2 = {d1:.4f}, "
            f"-> C{cluster_id + 1}"
        )

    new_centers = []
    for j in range(2):
        cluster_points = np.array(clusters[j], dtype=float)
        new_center = cluster_points.mean(axis=0)
        new_centers.append(new_center)

    new_centers = np.array(new_centers)
    return clusters, new_centers

def gaussian_rbf(x, y, cx, cy, sigma):
    r2 = (x - cx) ** 2 + (y - cy) ** 2
    return np.exp(-r2 / (2 * sigma ** 2))

def predict_values(X, Y, params):
    w0, w1, w2, c1x, c1y, c2x, c2y, sigma1, sigma2 = params

    phi1 = gaussian_rbf(X, Y, c1x, c1y, sigma1)
    phi2 = gaussian_rbf(X, Y, c2x, c2y, sigma2)
    z_hat = w0 + w1 * phi1 + w2 * phi2
    errors = z_hat - Z
    loss = 0.5 * np.mean(errors ** 2)

    return phi1, phi2, z_hat, errors, loss

def requested_gradients(X, Y, Z, params):
    w0, w1, w2, c1x, c1y, c2x, c2y, sigma1, sigma2 = params

    phi1 = gaussian_rbf(X, Y, c1x, c1y, sigma1)
    phi2 = gaussian_rbf(X, Y, c2x, c2y, sigma2)

    z_hat = w0 + w1 * phi1 + w2 * phi2
    e = z_hat - Z
    dL_dw0 = np.mean(e)
    dL_dw1 = np.mean(e * phi1)
    dL_dc2y = np.mean(e * w2 * phi2 * (Y - c2y) / (sigma2 ** 2))
    r2_sq = (X - c2x) ** 2 + (Y - c2y) ** 2
    dL_dsigma2 = np.mean(e * w2 * phi2 * r2_sq / (sigma2 ** 3))

    return dL_dc2y, dL_dsigma2, dL_dw0, dL_dw1

# ШАГ 1. K-MEANS
print_points()

centers = np.array([
    points[0],
    points[2]
], dtype=float)

print("Начальные центры K-Means:")
print(f"C1^(0) = ({centers[0,0]:.4f}, {centers[0,1]:.4f})")
print(f"C2^(0) = ({centers[1,0]:.4f}, {centers[1,1]:.4f})")
print()

for iteration in range(1, 6):
    print("=" * 70)
    print(f"Итерация K-Means #{iteration}")
    print("=" * 70)

    old_centers = centers.copy()
    clusters, centers = kmeans_step(points, centers)

    print("\nНовые центры:")
    for j in range(2):
        print(f"C{j+1} = ({centers[j,0]:.4f}, {centers[j,1]:.4f})")

    shift = np.linalg.norm(centers - old_centers)
    print(f"\nСмещение центров = {shift:.8f}\n")

    if shift < 1e-12:
        print("K-Means сошёлся.\n")
        break

centers = centers[np.argsort(centers[:, 0])]
(c1x, c1y), (c2x, c2y) = centers

print("=" * 70)
print("ИТОГОВЫЕ ЦЕНТРЫ")
print("=" * 70)
print(f"c1 = ({c1x:.6f}, {c1y:.6f})")
print(f"c2 = ({c2x:.6f}, {c2y:.6f})")
print()

# ШАГ 2. НАЧАЛЬНОЕ ПРИБЛИЖЕНИЕ
distance_centers = np.linalg.norm(centers[1] - centers[0])
sigma1 = distance_centers / 2
sigma2 = distance_centers / 2

w0 = 0.0
w1 = 0.1
w2 = -0.1
eta = 0.2

params = np.array([w0, w1, w2, c1x, c1y, c2x, c2y, sigma1, sigma2], dtype=float)

print("=" * 70)
print("НАЧАЛЬНОЕ ПРИБЛИЖЕНИЕ ДЛЯ ГРАДИЕНТНОГО СПУСКА")
print("=" * 70)
print(f"Расстояние между центрами = {distance_centers:.6f}")
print(f"sigma1 = {sigma1:.6f}")
print(f"sigma2 = {sigma2:.6f}")
print(f"w0 = {w0:.6f}")
print(f"w1 = {w1:.6f}")
print(f"w2 = {w2:.6f}")
print(f"eta = {eta:.6f}")
print()

# ШАГ 3. ЗНАЧЕНИЯ НА ПЕРВОЙ ИТЕРАЦИИ
phi1, phi2, z_hat, errors, loss = predict_values(X, Y, params)

print("=" * 70)
print("ПЕРВАЯ ИТЕРАЦИЯ: ЗНАЧЕНИЯ БАЗИСНЫХ ФУНКЦИЙ, ВЫХОДА И ОШИБОК")
print("=" * 70)
print(f"{'i':>2} | {'phi1':>10} | {'phi2':>10} | {'z_hat':>10} | {'e = z_hat-z':>12}")
print("-" * 70)
for i in range(m):
    print(
        f"{i+1:>2} | "
        f"{phi1[i]:>10.6f} | "
        f"{phi2[i]:>10.6f} | "
        f"{z_hat[i]:>10.6f} | "
        f"{errors[i]:>12.6f}"
    )

print(f"\nLoss = 0.5 * mean((z_hat - z)^2) = {loss:.10f}")
print()

# ШАГ 4. НУЖНЫЕ ПРОИЗВОДНЫЕ
dL_dc2y, dL_dsigma2, dL_dw0, dL_dw1 = requested_gradients(X, Y, Z, params)

print("=" * 70)
print("ЧАСТНЫЕ ПРОИЗВОДНЫЕ НА ПЕРВОЙ ИТЕРАЦИИ")
print("=" * 70)
print("Аналитические выражения:")
print("dL/dw0     = (1/m) * sum(e_i)")
print("dL/dw1     = (1/m) * sum(e_i * phi1_i)")
print("dL/dc2y    = (1/m) * sum(e_i * w2 * phi2_i * (y_i - c2y) / sigma2^2)")
print("dL/dsigma2 = (1/m) * sum(e_i * w2 * phi2_i * r2_i^2 / sigma2^3)")
print()

print("Численные значения:")
print(f"dL/dc2y    = {dL_dc2y:.10f}")
print(f"dL/dsigma2 = {dL_dsigma2:.10f}")
print(f"dL/dw0     = {dL_dw0:.10f}")
print(f"dL/dw1     = {dL_dw1:.10f}")
print()

# ШАГ 5. ОДИН ШАГ ГРАДИЕНТНОГО СПУСКА
w0_new = w0 - eta * dL_dw0
w1_new = w1 - eta * dL_dw1
c2y_new = c2y - eta * dL_dc2y
sigma2_new = sigma2 - eta * dL_dsigma2

print("=" * 70)
print("ОДИН ШАГ ГРАДИЕНТНОГО СПУСКА")
print("=" * 70)
print(f"w0_new     = {w0_new:.10f}")
print(f"w1_new     = {w1_new:.10f}")
print(f"c2y_new    = {c2y_new:.10f}")
print(f"sigma2_new = {sigma2_new:.10f}")