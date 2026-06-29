import numpy as np
import matplotlib.pyplot as plt


# Задача оптимизации
class Problem:
    def __init__(self, start_point):
        self.start_point = np.array(start_point, dtype=float)

    def f(self, point):
        x1, x2 = point

        return (2 * x1**2 + 2 * x1 * x2 + 3 * x2**2 - 12 * x1 - 6 * x2 + 18)

    def grad(self, point):
        x1, x2 = point

        return np.array([
            4 * x1 + 2 * x2 - 12,
            2 * x1 + 6 * x2 - 6
        ])

    def hessian(self):
        return np.array([
            [4.0, 2.0],
            [2.0, 6.0]
        ])


# Результат работы метода
class Result:
    def __init__(self, method_name, points, problem):
        self.method_name = method_name
        self.points = np.array(points)
        self.problem = problem

    def print_table(self):
        print("\n" + "=" * 80)
        print(self.method_name)
        print("=" * 80)
        print(f"{'k':>3} {'x1':>14} {'x2':>14} {'f(x1,x2)':>16} {'||grad||':>16}")
        print("-" * 80)

        for k, point in enumerate(self.points):
            value = self.problem.f(point)
            grad_norm = np.linalg.norm(self.problem.grad(point))

            print(
                f"{k:>3} "
                f"{point[0]:>14.8f} "
                f"{point[1]:>14.8f} "
                f"{value:>16.8f} "
                f"{grad_norm:>16.8f}"
            )

    def print_final(self):
        last = self.points[-1]

        print("\nИтог:")
        print(f"x* = ({last[0]:.8f}, {last[1]:.8f})")
        print(f"f(x*) = {self.problem.f(last):.8f}")
        print(f"||grad|| = {np.linalg.norm(self.problem.grad(last)):.8f}")
        print(f"Количество приближений: {len(self.points)}")


# Базовый класс метода оптимизации
class Optimizer:
    def __init__(self, problem, eps=0.0001, max_iter=1000):
        self.problem = problem
        self.eps = eps
        self.max_iter = max_iter
        self.name = "Базовый метод"

    def step(self, point, iteration):
        return point

    def solve(self):
        points = [self.problem.start_point.copy()]

        for k in range(self.max_iter):
            current = points[-1]
            grad_norm = np.linalg.norm(self.problem.grad(current))

            if grad_norm < self.eps:
                break

            next_point = self.step(current, k)
            points.append(next_point)

        return Result(self.name, points, self.problem)


# Метод покоординатного спуска
class CoordinateDescent(Optimizer):
    def __init__(self, problem, eps=0.0001, max_iter=1000):
        super().__init__(problem, eps, max_iter)
        self.name = "Метод покоординатного спуска"

    def step(self, point, iteration):
        next_point = point.copy()

        # Если итерация чётная — изменяем x1
        if iteration % 2 == 0:
            x2 = next_point[1]
            next_point[0] = 3 - x2 / 2

        # Если итерация нечётная — изменяем x2
        else:
            x1 = next_point[0]
            next_point[1] = 1 - x1 / 3

        return next_point


# Метод градиентного спуска
class GradientDescent(Optimizer):
    def __init__(self, problem, alpha=0.2, eps=0.0001, max_iter=1000):
        super().__init__(problem, eps, max_iter)
        self.name = "Метод градиентного спуска"
        self.alpha = alpha

    def step(self, point, iteration):
        gradient = self.problem.grad(point)

        return point - self.alpha * gradient


# Метод наискорейшего спуска
class SteepestDescent(Optimizer):
    def __init__(self, problem, eps=0.0001, max_iter=1000):
        super().__init__(problem, eps, max_iter)
        self.name = "Метод наискорейшего спуска"

    def step(self, point, iteration):
        gradient = self.problem.grad(point)
        H = self.problem.hessian()
        alpha = np.dot(gradient, gradient) / np.dot(gradient, H @ gradient)

        return point - alpha * gradient


# Визуализация результата
def plot_result(result):
    points = result.points
    problem = result.problem

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
    Z = (2 * X**2 + 2 * X * Y + 3 * Y**2 - 12 * X - 6 * Y + 18)

    plt.figure(figsize=(11, 7))
    levels = sorted(set([round(problem.f(p), 10) for p in points]))
    contour = plt.contour(X, Y, Z, levels=levels, cmap="viridis", linewidths=0.8, alpha=0.75)
    plt.clabel(contour, inline=True, fontsize=8)
    plt.plot(x_values, y_values, color="red", marker="o", markersize=5, linewidth=2.5)
    plt.scatter(x_values[0], y_values[0], color="red", s=60)
    plt.scatter(x_values[-1], y_values[-1], color="red", s=80)

    plt.title(result.method_name, fontsize=16)
    plt.xlabel("x1", fontsize=12)
    plt.ylabel("x2", fontsize=12)

    plt.grid(False)
    plt.show()


# Запуск программы
problem = Problem(start_point=[-2.0, 4.0])

methods = [
    CoordinateDescent(problem),
    GradientDescent(problem, alpha=0.2),
    SteepestDescent(problem)
]

for method in methods:
    result = method.solve()

    result.print_table()
    result.print_final()
    plot_result(result)