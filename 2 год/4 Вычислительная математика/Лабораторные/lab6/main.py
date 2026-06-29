import math
from pathlib import Path
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent

EQUATIONS = {
    1: {
        "name": "y' = y + x",
        "f": lambda x, y: y + x,
        "exact": lambda x, x0, y0: (y0 + x0 + 1) * math.exp(x - x0) - x - 1,
    },
    2: {
        "name": "y' = x - y",
        "f": lambda x, y: x - y,
        "exact": lambda x, x0, y0: x - 1 + (y0 - x0 + 1) * math.exp(-(x - x0)),
    },
    3: {
        "name": "y' = x * y",
        "f": lambda x, y: x * y,
        "exact": lambda x, x0, y0: y0 * math.exp((x * x - x0 * x0) / 2),
    },
    4: {
        "name": "y' = sin(x)",
        "f": lambda x, y: math.sin(x),
        "exact": lambda x, x0, y0: y0 + math.cos(x0) - math.cos(x),
    },
    5: {
        "name": "y' = cos(x)",
        "f": lambda x, y: math.cos(x),
        "exact": lambda x, x0, y0: y0 + math.sin(x) - math.sin(x0),
    },
    6: {
        "name": "y' = e^x - y",
        "f": lambda x, y: math.exp(x) - y,
        "exact": lambda x, x0, y0: 0.5 * math.exp(x) + (y0 - 0.5 * math.exp(x0)) * math.exp(x0 - x),
    },
    7: {
        "name": "y' = y + sin(x)",
        "f": lambda x, y: y + math.sin(x),
        "exact": lambda x, x0, y0: (
            (y0 + 0.5 * (math.sin(x0) + math.cos(x0))) * math.exp(x - x0)
            - 0.5 * (math.sin(x) + math.cos(x))
        ),
    },
    8: {
        "name": "y' = e^(-x) * y",
        "f": lambda x, y: math.exp(-x) * y,
        "exact": lambda x, x0, y0: y0 * math.exp(math.exp(-x0) - math.exp(-x)),
    },
}


def improved_euler(f, x0, y0, xn, n):
    h = (xn - x0) / n
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [y0]

    for i in range(n):
        x = xs[i]
        y = ys[i]

        k1 = f(x, y)
        k2 = f(x + h, y + h * k1)
        ys.append(y + h * (k1 + k2) / 2)

    return xs, ys


def runge_kutta_4(f, x0, y0, xn, n):
    h = (xn - x0) / n
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [y0]

    for i in range(n):
        x = xs[i]
        y = ys[i]

        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)

        ys.append(y + (k1 + 2 * k2 + 2 * k3 + k4) / 6)

    return xs, ys


def milne(f, x0, y0, xn, n, eps):
    h = (xn - x0) / n
    xs = [x0 + i * h for i in range(n + 1)]

    _, ys = runge_kutta_4(f, x0, y0, x0 + 3 * h, 3)

    for i in range(3, n):
        y_pred = ys[i - 3] + 4 * h * (2 * f(xs[i], ys[i]) - f(xs[i - 1], ys[i - 1]) + 2 * f(xs[i - 2], ys[i - 2])) / 3

        y_corr = y_pred

        for _ in range(50):
            old = y_corr
            y_corr = ys[i - 1] + h * (f(xs[i - 1], ys[i - 1]) + 4 * f(xs[i], ys[i]) + f(xs[i + 1], old)) / 3

            if abs(y_corr - old) <= eps:
                break

        ys.append(y_corr)

    return xs, ys


def validate(p):
    if p["equation"] not in EQUATIONS:
        raise ValueError("неверный номер уравнения")
    if p["xn"] <= p["x0"]:
        raise ValueError("должно выполняться условие xn > x0")
    if p["h"] <= 0:
        raise ValueError("шаг h должен быть положительным")
    if p["eps"] <= 0:
        raise ValueError("точность eps должна быть положительной")

    n = math.ceil((p["xn"] - p["x0"]) / p["h"])

    if n < 4:
        raise ValueError("слишком большой шаг h: для метода Милна нужно минимум 4 шага")
    if n > 100000:
        raise ValueError("слишком маленький шаг h: слишком много точек")

    return n


def max_error(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def runge_error(method, f, x0, y0, xn, n, order):
    _, y_h = method(f, x0, y0, xn, n)
    _, y_h2 = method(f, x0, y0, xn, 2 * n)

    return max(
        abs(y_h2[2 * i] - y_h[i]) / (2 ** order - 1)
        for i in range(n + 1)
    )


def read_int(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Ошибка: нужно ввести целое число.")


def read_float(text):
    while True:
        try:
            return float(input(text).replace(",", "."))
        except ValueError:
            print("Ошибка: нужно ввести число.")


def print_equations():
    print("\nДоступные уравнения:")

    for number, eq in EQUATIONS.items():
        print(f"{number}. {eq['name']}")


def read_from_console():
    while True:
        print_equations()

        p = {
            "equation": read_int("Номер уравнения: "),
            "x0": read_float("x0 = "),
            "y0": read_float("y0 = "),
            "xn": read_float("xn = "),
            "h": read_float("h = "),
            "eps": read_float("eps = "),
        }

        try:
            validate(p)
            return p
        except ValueError as error:
            print(f"\nОшибка: {error}. Введите данные заново.")


def find_file(filename):
    path = Path(filename.strip().strip('"'))

    if path.exists():
        return path

    path = BASE_DIR / path

    if path.exists():
        return path

    raise FileNotFoundError(
        f"файл не найден\n"
        f"Папка запуска: {Path.cwd()}\n"
        f"Папка программы: {BASE_DIR}"
    )


def read_from_file():
    while True:
        try:
            path = find_file(input("Имя файла: "))

            p = {}

            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()

                if "=" in line:
                    key, value = line.split("=", 1)
                else:
                    key, value = line.split()

                key = key.strip().lower()
                value = value.strip().replace(",", ".")

                if key in ("equation", "eq"):
                    p["equation"] = int(value)
                elif key in ("x0", "y0", "xn", "h", "eps"):
                    p[key] = float(value)
                else:
                    raise ValueError(f"неизвестный параметр: {key}")

            missing = {"equation", "x0", "y0", "xn", "h", "eps"} - p.keys()

            if missing:
                raise ValueError("нет параметров: " + ", ".join(sorted(missing)))

            validate(p)
            print(f"Файл прочитан: {path}")
            return p

        except Exception as error:
            print(f"\nОшибка чтения файла: {error}")
            print("Попробуйте снова.\n")


def print_table(xs, exact, euler, rk4, milne_values):
    print("\nТаблица значений:")
    print(f"{'i':>3} {'x':>9} {'точное':>13} {'Эйлер ус.':>13} {'РК4':>13} {'Милн':>13}")

    rows = list(range(len(xs)))

    if len(rows) > 31:
        rows = rows[:15] + [None] + rows[-10:]

    for i in rows:
        if i is None:
            print("...")
            continue

        print(
            f"{i:3d} {xs[i]:9.4f} {exact[i]:13.6f} "
            f"{euler[i]:13.6f} {rk4[i]:13.6f} {milne_values[i]:13.6f}"
        )


def show_plot(xs, exact, euler, rk4, milne_values):
    plt.figure(figsize=(9, 6))
    plt.plot(xs, exact, label="Точное решение", linewidth=2)
    plt.plot(xs, euler, "o-", markersize=3, label="Усовершенствованный Эйлер")
    plt.plot(xs, rk4, "s-", markersize=3, label="Рунге-Кутта 4")
    plt.plot(xs, milne_values, "^-", markersize=3, label="Милн")

    plt.title("Численное решение задачи Коши")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


def solve(p):
    n = validate(p)
    h = (p["xn"] - p["x0"]) / n

    eq = EQUATIONS[p["equation"]]
    f = eq["f"]
    exact_func = eq["exact"]

    x0 = p["x0"]
    y0 = p["y0"]
    xn = p["xn"]
    eps = p["eps"]

    xs, euler = improved_euler(f, x0, y0, xn, n)
    _, rk4 = runge_kutta_4(f, x0, y0, xn, n)
    _, milne_values = milne(f, x0, y0, xn, n, eps)

    exact = [exact_func(x, x0, y0) for x in xs]

    euler_runge = runge_error(improved_euler, f, x0, y0, xn, n, 2)
    rk4_runge = runge_error(runge_kutta_4, f, x0, y0, xn, n, 4)
    milne_error = max_error(exact, milne_values)

    print("\nИсходные данные:")
    print(f"Уравнение: {eq['name']}")
    print(f"x0 = {x0}, y0 = {y0}, xn = {xn}, h = {h:.8f}, eps = {eps}")
    print(f"Количество шагов n = {n}")

    print_table(xs, exact, euler, rk4, milne_values)

    print("\nПогрешности:")
    print(f"Усовершенствованный Эйлер, правило Рунге: {euler_runge:.8e}")
    print(f"Рунге-Кутта 4, правило Рунге:             {rk4_runge:.8e}")
    print(f"Милн, max |y точн. - y прибл.|:          {milne_error:.8e}")

    print("\nСравнение с eps:")
    print("Эйлер ус.:", "достигнута" if euler_runge <= eps else "не достигнута")
    print("РК4:      ", "достигнута" if rk4_runge <= eps else "не достигнута")
    print("Милн:     ", "достигнута" if milne_error <= eps else "не достигнута")

    show_plot(xs, exact, euler, rk4, milne_values)


def main():
    print("ЛР №6. Вариант 2. Численное решение ОДУ")

    while True:
        print("\n1 - ввод с консоли")
        print("2 - ввод из файла")
        print("0 - выход")

        mode = input("Выберите действие: ")

        if mode == "1":
            solve(read_from_console())
        elif mode == "2":
            solve(read_from_file())
        elif mode == "0":
            print("Работа программы завершена.")
            break
        else:
            print("Ошибка: выберите 0, 1 или 2.")


if __name__ == "__main__":
    main()
