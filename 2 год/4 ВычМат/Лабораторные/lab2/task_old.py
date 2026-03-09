import math
import numpy as np
import matplotlib.pyplot as plt


EQUATIONS = {
    1: {
        "name": "-1.38*x^3 - 5.42*x^2 + 2.57*x + 10.95",
        "f": lambda x: -1.38 * x**3 - 5.42 * x**2 + 2.57 * x + 10.95,
        "df": lambda x: -4.14 * x**2 - 10.84 * x + 2.57,
        "plot_range": (-5, 3),
    },
    2: {
        "name": "x^3 - 1.89*x^2 - 2*x + 1.76",
        "f": lambda x: x**3 - 1.89 * x**2 - 2 * x + 1.76,
        "df": lambda x: 3 * x**2 - 3.78 * x - 2,
        "plot_range": (-3, 4),
    },
    3: {
        "name": "cos(x) - x",
        "f": lambda x: math.cos(x) - x,
        "df": lambda x: -math.sin(x) - 1,
        "plot_range": (-3, 3),
    },
    4: {
        "name": "exp(x) - 3*x",
        "f": lambda x: math.exp(x) - 3 * x,
        "df": lambda x: math.exp(x) - 3,
        "plot_range": (-1, 2),
    },
}


def sys1_f1(x, y):
    return math.sin(x + 1) - y - 1.2

def sys1_f2(x, y):
    return 2 * x + math.cos(y) - 2

def sys1_phi1(x, y):
    return 1 - math.cos(y) / 2

def sys1_phi2(x, y):
    return math.sin(x + 1) - 1.2

def sys1_dphi(x, y):
    return [[0.0, math.sin(y) / 2], [math.cos(x + 1), 0.0],]


def sys2_f1(x, y):
    return math.cos(x - 1) + y - 0.5

def sys2_f2(x, y):
    return x - math.cos(y) - 3

def sys2_phi1(x, y):
    return 3 + math.cos(y)

def sys2_phi2(x, y):
    return 0.5 - math.cos(x - 1)

def sys2_dphi(x, y):
    return [[0.0, -math.sin(y)], [math.sin(x - 1), 0.0],]


SYSTEMS = {
    1: {
        "name": "sin(x + 1) - y = 1.2; 2x + cos(y) = 2",
        "f1": sys1_f1,
        "f2": sys1_f2,
        "phi1": sys1_phi1,
        "phi2": sys1_phi2,
        "dphi": sys1_dphi,
        "xlim": (-1, 2),
        "ylim": (-2, 1),
    },
    2: {
        "name": "cos(x - 1) + y = 0.5; x - cos(y) = 3",
        "f1": sys2_f1,
        "f2": sys2_f2,
        "phi1": sys2_phi1,
        "phi2": sys2_phi2,
        "dphi": sys2_dphi,
        "xlim": (1.5, 4.5),
        "ylim": (-2, 1),
    },
}


def read_from_file(path, count):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().replace(",", ".")
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    except OSError as e:
        raise OSError(f"Не удалось открыть файл: {e}")

    parts = text.split()
    if len(parts) < count:
        raise ValueError(f"В файле должно быть минимум {count} чисел")

    numbers = []
    for i in range(count):
        try:
            numbers.append(float(parts[i]))
        except ValueError:
            raise ValueError("В файле должны быть только числа")
    return numbers


def read_float(prompt):
    value = input(prompt).strip().replace(",", ".")
    try:
        return float(value)
    except ValueError:
        raise ValueError("Нужно ввести число")


def read_choice(prompt, valid_choices):
    value = input(prompt).strip()
    if value not in valid_choices:
        raise ValueError("Неверный выбор")
    return value


def count_roots(f, a, b, samples=2000):
    xs = np.linspace(a, b, samples)
    values = []

    for x in xs:
        try:
            y = f(float(x))
            values.append(y if math.isfinite(y) else None)
        except Exception:
            values.append(None)

    changes = 0
    for i in range(len(values) - 1):
        y1, y2 = values[i], values[i + 1]
        if y1 is None or y2 is None:
            continue
        if y1 == 0 or y1 * y2 < 0:
            changes += 1
    return changes


def plot_equation(eq):
    left, right = eq["plot_range"]
    xs = np.linspace(left, right, 1000)
    ys = []

    for x in xs:
        try:
            ys.append(eq["f"](float(x)))
        except Exception:
            ys.append(np.nan)

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label=eq["name"])
    plt.axhline(0)
    plt.axvline(0)
    plt.grid(True)
    plt.legend()
    plt.title("График функции")
    plt.show()


def plot_system(system):
    x = np.linspace(system["xlim"][0], system["xlim"][1], 400)
    y = np.linspace(system["ylim"][0], system["ylim"][1], 400)
    X, Y = np.meshgrid(x, y)

    F1 = np.vectorize(system["f1"])(X, Y)
    F2 = np.vectorize(system["f2"])(X, Y)

    plt.figure(figsize=(7, 6))
    plt.contour(X, Y, F1, levels=[0])
    plt.contour(X, Y, F2, levels=[0])
    plt.grid(True)
    plt.title("График системы")
    plt.show()




# методы для уравнения
def bisection(f, a, b, eps, max_iter=1000):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None, 0, "На концах интервала нет смены знака"

    iterations = 0
    while abs(b - a) > eps and iterations < max_iter:
        x = (a + b) / 2
        fx = f(x)
        iterations += 1
        if fa * fx <= 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    return (a + b) / 2, iterations, None


def newton(f, df, x0, eps, max_iter=1000):
    x = x0
    iterations = 0

    while iterations < max_iter:
        dfx = df(x)
        if abs(dfx) < 1e-12:
            return None, iterations, "Производная слишком мала"
        x_next = x - f(x) / dfx
        iterations += 1
        if abs(x_next - x) < eps:
            return x_next, iterations, None
        x = x_next

    return None, iterations, "Превышено число итераций"


def simple_iteration_equation(f, df, a, b, eps, max_iter=1000):
    xs = np.linspace(a, b, 1000)
    dvals = np.array([abs(df(float(x))) for x in xs])
    m = np.max(dvals)

    if m == 0:
        return None, 0, "Не удалось выбрать lambda"

    d_mid = df((a + b) / 2)
    lambd = -1 / m if d_mid > 0 else 1 / m

    def phi(x):
        return x + lambd * f(x)

    q = np.max([abs(1 + lambd * df(float(x))) for x in xs])
    if q >= 1:
        return None, 0, f"Условие сходимости не выполнено: q = {q:.6f}"

    x = (a + b) / 2
    iterations = 0
    while iterations < max_iter:
        x_next = phi(x)
        iterations += 1
        if abs(x_next - x) < eps:
            return x_next, iterations, None
        x = x_next

    return None, iterations, "Превышено число итераций"



# методы для системы
def system_convergence_check(system, x0, y0, dx=0.2, dy=0.2, samples=20):
    xs = np.linspace(x0 - dx, x0 + dx, samples)
    ys = np.linspace(y0 - dy, y0 + dy, samples)
    q = 0.0

    for x in xs:
        for y in ys:
            try:
                d = system["dphi"](float(x), float(y))
                s1 = abs(d[0][0]) + abs(d[0][1])
                s2 = abs(d[1][0]) + abs(d[1][1])
                q = max(q, s1, s2)
            except Exception:
                pass
    return q


def simple_iteration_system(system, x0, y0, eps, max_iter=1000):
    q = system_convergence_check(system, x0, y0)
    if q >= 1:
        return None, None, 0, None, f"Условие сходимости не выполнено: q = {q:.6f}"

    x, y = x0, y0
    iterations = 0

    while iterations < max_iter:
        x_next = system["phi1"](x, y)
        y_next = system["phi2"](x, y)
        dx = abs(x_next - x)
        dy = abs(y_next - y)
        iterations += 1

        if max(dx, dy) < eps:
            return x_next, y_next, iterations, (dx, dy), None

        x, y = x_next, y_next

    return None, None, iterations, None, "Превышено число итераций"



def choose_input_mode():
    print("Выберите ввод:")
    print("1 — клавиатура")
    print("2 — файл")
    return read_choice("Ваш выбор: ", {"1", "2"})


def get_equation_input():
    mode = choose_input_mode()
    if mode == "1":
        a = read_float("Введите левую границу a: ")
        b = read_float("Введите правую границу b: ")
        eps = read_float("Введите точность eps: ")
        return a, b, eps

    path = input("Введите путь к txt файлу: ").strip()
    return read_from_file(path, 3)


def get_system_input():
    mode = choose_input_mode()
    if mode == "1":
        x0 = read_float("Введите начальное приближение x0: ")
        y0 = read_float("Введите начальное приближение y0: ")
        eps = read_float("Введите точность eps: ")
        return x0, y0, eps

    path = input("Введите путь к txt файлу: ").strip()
    return read_from_file(path, 3)



# решениие уравнения
def solve_equation_menu():
    print("\nДоступные уравнения:")
    for k, eq in EQUATIONS.items():
        print(f"{k} — {eq['name']}")

    eq_num = int(read_choice("Выберите уравнение: ", {"1", "2", "3", "4"}))
    eq = EQUATIONS[eq_num]

    print("\nМетоды для варианта 2:")
    print("1 — метод половинного деления")
    print("3 — метод Ньютона")
    print("5 — метод простой итерации")
    method = read_choice("Выберите метод: ", {"1", "3", "5"})

    a, b, eps = get_equation_input()
    if a >= b:
        raise ValueError("Левая граница должна быть меньше правой")
    if eps <= 0:
        raise ValueError("Точность должна быть положительной")

    plot_equation(eq)

    roots_count = count_roots(eq["f"], a, b)
    if roots_count == 0:
        print("На интервале корней не найдено")
        return
    if roots_count > 1:
        print("На интервале найдено несколько корней")
        return

    if method == "1":
        root, iterations, error = bisection(eq["f"], a, b, eps)
    elif method == "3":
        x0 = (a + b) / 2
        root, iterations, error = newton(eq["f"], eq["df"], x0, eps)
    else:
        root, iterations, error = simple_iteration_equation(eq["f"], eq["df"], a, b, eps)

    if error:
        print("Ошибка:", error)
        return

    print("\nРезультат:")
    print(f"Корень: {root:.10f}")
    print(f"f(x): {eq['f'](root):.10f}")
    print(f"Итераций: {iterations}")


# решение системы
def solve_system_menu():
    print("\nДоступные системы:")
    for k, system in SYSTEMS.items():
        print(f"{k} — {system['name']}")

    sys_num = int(read_choice("Выберите систему: ", {"1", "2"}))
    system = SYSTEMS[sys_num]

    print("\nДля варианта 2 используется метод 7 — простая итерация для систем.")
    x0, y0, eps = get_system_input()

    if eps <= 0:
        raise ValueError("Точность должна быть положительной")

    plot_system(system)

    x, y, iterations, errors, error = simple_iteration_system(system, x0, y0, eps)
    if error:
        print("Ошибка:", error)
        return

    print("\nРезультат:")
    print(f"x = {x:.10f}")
    print(f"y = {y:.10f}")
    print(f"Итераций: {iterations}")
    print(f"Вектор погрешностей: ({errors[0]:.10f}, {errors[1]:.10f})")
    print(f"Проверка f1(x, y) = {system['f1'](x, y):.10f}")
    print(f"Проверка f2(x, y) = {system['f2'](x, y):.10f}")



def main():
    print("Выберите тип задачи:")
    print("1 — нелинейное уравнение")
    print("2 — система нелинейных уравнений")
    choice = read_choice("Ваш выбор: ", {"1", "2"})

    if choice == "1":
        solve_equation_menu()
    else:
        solve_system_menu()


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print("Ошибка:", e)
    except ValueError as e:
        print("Ошибка ввода:", e)
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    except Exception as e:
        print("Непредвиденная ошибка:", e)
