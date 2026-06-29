import numpy as np


EPS = 0.0001
MAX_ITER = 100
start = np.array([5.5, 2.5], dtype=float)


def z(point):
    x, y = point
    return (x**3 - 15 * x**2 + 72 * x + y**3 - 5 * y**2 + 7 * y - 115)


def grad(point):
    x, y = point

    dz_dx = 3 * x**2 - 30 * x + 72
    dz_dy = 3 * y**2 - 10 * y + 7

    return np.array([dz_dx, dz_dy], dtype=float)


# Матрица Гессе
def hessian(point):
    x, y = point
    return np.array([
        [6 * x - 30, 0],
        [0, 6 * y - 10]
    ], dtype=float)


# Метод Ньютона
def newton_method(start_point, eps=EPS, max_iter=MAX_ITER):
    point = start_point.copy()
    iterations = []

    for k in range(max_iter + 1):
        g = grad(point)
        H = hessian(point)
        grad_norm = np.linalg.norm(g)

        iterations.append({
            "k": k,
            "x": point[0],
            "y": point[1],
            "z": z(point),
            "grad_x": g[0],
            "grad_y": g[1],
            "grad_norm": grad_norm
        })

        if grad_norm < eps:
            break

        delta = np.linalg.solve(H, g)
        point = point - delta

    return iterations


# Классификация стационарной точки
def classify_stationary_point(point):
    H = hessian(point)

    det_H = np.linalg.det(H)
    h11 = H[0, 0]

    if det_H > 0 and h11 > 0:
        return "локальный минимум"
    elif det_H > 0 and h11 < 0:
        return "локальный максимум"
    elif det_H < 0:
        return "седловая точка"
    else:
        return "требуется дополнительное исследование"


# Аналитический поиск стационарных точек
def find_stationary_points():
    x_values = [4.0, 6.0]
    y_values = [1.0, 7.0 / 3.0]
    points = []

    for x in x_values:
        for y in y_values:
            points.append(np.array([x, y], dtype=float))

    return points


# Запуск метода Ньютона
iterations = newton_method(start)


# Таблица итераций метода Ньютона
print("Метод Ньютона")
print("=" * 100)
print(
    f"{'k':>3} "
    f"{'x':>14} "
    f"{'y':>14} "
    f"{'z(x,y)':>16} "
    f"{'grad_x':>14} "
    f"{'grad_y':>14} "
    f"{'||grad||':>14}"
)
print("-" * 100)

for row in iterations:
    print(
        f"{row['k']:>3} "
        f"{row['x']:>14.8f} "
        f"{row['y']:>14.8f} "
        f"{row['z']:>16.8f} "
        f"{row['grad_x']:>14.8f} "
        f"{row['grad_y']:>14.8f} "
        f"{row['grad_norm']:>14.8f}"
    )


# Итог метода Ньютона
last = iterations[-1]

print("\nРезультат метода Ньютона:")
print("-" * 100)
print(f"x* = {last['x']:.8f}")
print(f"y* = {last['y']:.8f}")
print(f"z(x*, y*) = {last['z']:.8f}")
print(f"||grad|| = {last['grad_norm']:.8f}")
print(f"Количество итераций: {last['k']}")


# Аналитические стационарные точки
stationary_points = find_stationary_points()

print("\nСтационарные точки и их типы:")
print("=" * 100)
print(
    f"{'x':>14} "
    f"{'y':>14} "
    f"{'z(x,y)':>16} "
    f"{'det(H)':>14} "
    f"{'тип точки':>30}"
)
print("-" * 100)

for point in stationary_points:
    H = hessian(point)
    det_H = np.linalg.det(H)
    point_type = classify_stationary_point(point)

    print(
        f"{point[0]:>14.8f} "
        f"{point[1]:>14.8f} "
        f"{z(point):>16.8f} "
        f"{det_H:>14.8f} "
        f"{point_type:>30}"
    )