import math
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x**3 - 3 * np.sin(x)

def df(x):
    return 3 * x**2 - 3 * np.cos(x)


# Кубическая аппроксимация Эрмита
def cubic_approximation(x, a, b):
    t = (x - a) / (b - a)

    fa = f(a)
    fb = f(b)
    dfa = df(a)
    dfb = df(b)

    return ((2 * t**3 - 3 * t**2 + 1) * fa + (t**3 - 2 * t**2 + t) * (b - a) * dfa + (-2 * t**3 + 3 * t**2) * fb + (t**3 - t**2) * (b - a) * dfb)


# Один шаг метода кубической аппроксимации
def cubic_step(a, b):
    fa = f(a)
    fb = f(b)

    dfa = df(a)
    dfb = df(b)

    z = 3 * (fa - fb) / (b - a) + dfa + dfb
    w = math.sqrt(z**2 - dfa * dfb)
    x = b - (b - a) * (dfb + w - z) / (dfb - dfa + 2 * w)

    return x


# Метод кубической аппроксимации
def cubic_approximation_method(a0, b0, eps=0.0001, max_iter=100):
    a = a0
    b = b0

    iterations = []

    for k in range(1, max_iter + 1):
        x = cubic_step(a, b)

        fx = f(x)
        dfx = df(x)

        iterations.append({"k": k, "a": a, "b": b, "x": x, "fx": fx, "dfx": dfx})

        if abs(dfx) < eps:
            break

        if dfx > 0:
            b = x
        else:
            a = x

    return iterations



a0 = 0
b0 = 1
eps = 0.0001

iterations = cubic_approximation_method(a0, b0, eps)

print("Таблица итераций:")
print("-" * 75)
print(f"{'k':>3} {'a':>12} {'b':>12} {'x':>12} {'f(x)':>14} {'df(x)':>14}")
print("-" * 75)

for row in iterations:
    print(
        f"{row['k']:>3} "
        f"{row['a']:>12.6f} "
        f"{row['b']:>12.6f} "
        f"{row['x']:>12.6f} "
        f"{row['fx']:>14.6f} "
        f"{row['dfx']:>14.6f}"
    )

last = iterations[-1]

print("\nРезультат:")
print(f"x* = {last['x']:.6f}")
print(f"f(x*) = {last['fx']:.6f}")
print(f"|f'(x*)| = {abs(last['dfx']):.8f}")


# Визуализация одной итерации
def plot_iteration(iteration):
    a = iteration["a"]
    b = iteration["b"]
    x_min = iteration["x"]
    xs = np.linspace(a, b, 400)
    ys = f(xs)
    ps = cubic_approximation(xs, a, b)

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label="Исходная функция f(x)", linewidth=2)
    plt.plot(xs, ps, "--", label="Кубическая аппроксимация P(x)", linewidth=2)
    plt.scatter([a, b], [f(a), f(b)], label="Концы текущего отрезка")
    plt.scatter([x_min], [f(x_min)], label="Новое приближение x_k")
    plt.title(f"Кубическая аппроксимация, итерация {iteration['k']}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


# Построение графиков для всех итераций
for iteration in iterations:
    plot_iteration(iteration)