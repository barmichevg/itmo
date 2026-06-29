import numpy as np
import matplotlib.pyplot as plt


EPS = 0.0001
MAX_ITER = 1000
x0 = np.array([-2.0, 4.0])
H = np.array([[4.0, 2.0], [2.0, 6.0]])


def f(x, y):
    return 2 * x**2 + 2 * x * y + 3 * y**2 - 12 * x - 6 * y + 18

def f_point(p):
    return f(p[0], p[1])


def grad(p):
    x, y = p

    df_dx = 4 * x + 2 * y - 12
    df_dy = 2 * x + 6 * y - 6

    return np.array([df_dx, df_dy])


# Метод покоординатного спуска
def coordinate_descent(start, eps=EPS, max_iter=MAX_ITER):
    points = [start.copy()]

    for _ in range(max_iter):
        current = points[-1].copy()

        if np.linalg.norm(grad(current)) < eps:
            break

        # Минимизация по x1 при фиксированном x2
        current[0] = 3 - current[1] / 2
        points.append(current.copy())

        if np.linalg.norm(grad(current)) < eps:
            break

        # Минимизация по x2 при фиксированном x1
        current[1] = 1 - current[0] / 3
        points.append(current.copy())

    return np.array(points)


# Метод градиентного спуска
def gradient_descent(start, alpha=0.2, eps=EPS, max_iter=MAX_ITER):
    points = [start.copy()]

    for _ in range(max_iter):
        current = points[-1].copy()
        g = grad(current)

        if np.linalg.norm(g) < eps:
            break

        next_point = current - alpha * g
        points.append(next_point)

    return np.array(points)


# Метод наискорейшего спуска
def steepest_descent(start, eps=EPS, max_iter=MAX_ITER):
    points = [start.copy()]

    for _ in range(max_iter):
        current = points[-1].copy()
        g = grad(current)

        if np.linalg.norm(g) < eps:
            break

        alpha = np.dot(g, g) / np.dot(g, H @ g)
        next_point = current - alpha * g
        points.append(next_point)

    return np.array(points)


# Таблицы
def print_table(method_name, points):
    print("\n" + "=" * 80)
    print(method_name)
    print("=" * 80)
    print(f"{'k':>3} {'x1':>14} {'x2':>14} {'f(x1,x2)':>16} {'||grad||':>16}")
    print("-" * 80)

    for k, p in enumerate(points):
        print(
            f"{k:>3} "
            f"{p[0]:>14.8f} "
            f"{p[1]:>14.8f} "
            f"{f_point(p):>16.8f} "
            f"{np.linalg.norm(grad(p)):>16.8f}"
        )


# Визуализация
def plot_method(points, method_name):
    x_values = points[:, 0]
    y_values = points[:, 1]

    minimum = np.array([3.0, 0.0])

    all_x = np.append(x_values, minimum[0])
    all_y = np.append(y_values, minimum[1])

    x_min = all_x.min() - 3
    x_max = all_x.max() + 3
    y_min = all_y.min() - 3
    y_max = all_y.max() + 3

    X, Y = np.meshgrid(np.linspace(x_min, x_max, 600), np.linspace(y_min, y_max, 600))
    Z = f(X, Y)

    plt.figure(figsize=(11, 7))

    levels = sorted(set([round(f_point(p), 10) for p in points]))
    contour = plt.contour(X, Y, Z, levels=levels, cmap="viridis", linewidths=0.8, alpha=0.75)

    plt.clabel(contour, inline=True, fontsize=8)
    plt.plot(x_values, y_values, color="red", marker="o", markersize=5, linewidth=2.5)
    plt.scatter(x_values[0], y_values[0], color="red", s=60)
    plt.scatter(x_values[-1], y_values[-1], color="red", s=80)

    plt.title(f"{method_name}", fontsize=16)
    plt.xlabel("x1", fontsize=12)
    plt.ylabel("x2", fontsize=12)

    plt.grid(False)
    plt.show()


coordinate_points = coordinate_descent(x0)
gradient_points = gradient_descent(x0, alpha=0.2)
steepest_points = steepest_descent(x0)


# Вывод таблиц
print_table("Метод покоординатного спуска", coordinate_points)
print_table("Метод градиентного спуска", gradient_points)
print_table("Метод наискорейшего спуска", steepest_points)


# Построение графиков
plot_method(coordinate_points, "Метод покоординатного спуска")
plot_method(gradient_points, "Метод градиентного спуска")
plot_method(steepest_points, "Метод наискорейшего спуска")


# Итоговые результаты
print("\nИтоговые результаты:")
print("-" * 80)

methods = [("Покоординатный спуск", coordinate_points), ("Градиентный спуск", gradient_points), ("Наискорейший спуск", steepest_points)]

for name, points in methods:
    last = points[-1]

    print(f"{name}:")
    print(f"  Количество приближений: {len(points)}")
    print(f"  x* = ({last[0]:.8f}, {last[1]:.8f})")
    print(f"  f(x*) = {f_point(last):.8f}")
    print(f"  ||grad|| = {np.linalg.norm(grad(last)):.8f}")
    print()