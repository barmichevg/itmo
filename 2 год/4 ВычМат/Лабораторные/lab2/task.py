import math
import numpy as np
import matplotlib.pyplot as plt



EQUATIONS = {
    1: {
        "name": "-1.38*x^3 - 5.42*x^2 + 2.57*x + 10.95",
        "f": lambda x: -1.38 * x**3 - 5.42 * x**2 + 2.57 * x + 10.95,
        "df": lambda x: -4.14 * x**2 - 10.84 * x + 2.57,
    },
    2: {
        "name": "x^3 - 1.89*x^2 - 2*x + 1.76",
        "f": lambda x: x**3 - 1.89 * x**2 - 2 * x + 1.76,
        "df": lambda x: 3 * x**2 - 3.78 * x - 2,
    },
    3: {
        "name": "cos(x) - x",
        "f": lambda x: math.cos(x) - x,
        "df": lambda x: -math.sin(x) - 1,
    },
    4: {
        "name": "exp(x) - 3*x",
        "f": lambda x: math.exp(x) - 3 * x,
        "df": lambda x: math.exp(x) - 3,
    },
}

SYSTEMS = {
    1: {
        "name": "sin(x + 1) - y = 1.2; 2x + cos(y) = 2",
        "f1": lambda x, y: math.sin(x + 1) - y - 1.2,
        "f2": lambda x, y: 2 * x + math.cos(y) - 2,
        "phi1": lambda x, y: 1 - math.cos(y) / 2,
        "phi2": lambda x, y: math.sin(x + 1) - 1.2,
        "dphi": lambda x, y: [[0.0, math.sin(y) / 2], [math.cos(x + 1), 0.0]],
        "xlim": (-1, 2),
        "ylim": (-2, 1),
    },
    2: {
        "name": "cos(x - 1) + y = 0.5; x - cos(y) = 3",
        "f1": lambda x, y: math.cos(x - 1) + y - 0.5,
        "f2": lambda x, y: x - math.cos(y) - 3,
        "phi1": lambda x, y: 3 + math.cos(y),
        "phi2": lambda x, y: 0.5 - math.cos(x - 1),
        "dphi": lambda x, y: [[0.0, -math.sin(y)], [math.sin(x - 1), 0.0]],
        "xlim": (1.5, 4.5),
        "ylim": (-2, 1),
    },
}


def ask_choice(prompt, choices):
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        
        print("Неверный выбор. Попробуйте снова.")


def ask_float(prompt, positive=False):
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if positive and value <= 0:
                print("Введите заново.")
                continue
            return value
        
        except ValueError:
            print("Введите заново.")


def ask_interval():
    while True:
        a = ask_float("Введите левую границу a: ")
        b = ask_float("Введите правую границу b: ")
        if a < b:
            return a, b
        
        print("Правая граница должна быть больше левой.")


def read_config(path):
    cfg = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError
            
            k, v = line.split("=", 1)
            cfg[k.strip().lower()] = v.strip().replace(",", ".")

    if not cfg:
        raise ValueError
    return cfg


def ask_config():
    while True:
        path = input("Введите путь к txt файлу: ").strip()
        try:
            return read_config(path)
        except Exception:
            print("Введите путь заново.")


def count_roots(f, a, b, samples=2000):
    xs = np.linspace(a, b, samples)
    ys = []
    for x in xs:
        try:
            y = f(float(x))
            ys.append(y if math.isfinite(y) else np.nan)
        except Exception:
            ys.append(np.nan)

    changes = 0
    for y1, y2 in zip(ys, ys[1:]):
        if not (np.isfinite(y1) and np.isfinite(y2)):
            continue
        if y1 == 0 or y1 * y2 < 0:
            changes += 1
    return changes


def plot_equation(eq, a, b, root=None):
    xs = np.linspace(a, b, 2000)
    ys = np.array([eq["f"](float(x)) for x in xs], dtype=float)
    finite = ys[np.isfinite(ys)]
    ymin, ymax = float(np.min(finite)), float(np.max(finite))
    if ymin == ymax:
        ymin -= 1
        ymax += 1
    pad = 0.05 * (ymax - ymin)

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label=eq["name"])
    if root is not None:
        plt.plot(root, eq["f"](root), "o", label=f"x = {root:.4f}")
    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.xlim(a, b)
    plt.ylim(ymin - pad, ymax + pad)
    plt.grid(True)
    plt.legend()
    plt.title(f"График на [{a:.3f}; {b:.3f}]")
    plt.show()


def plot_system(system, point=None):
    x1, x2 = system["xlim"]
    y1, y2 = system["ylim"]
    x = np.linspace(x1, x2, 500)
    y = np.linspace(y1, y2, 500)
    X, Y = np.meshgrid(x, y)
    F1 = np.vectorize(system["f1"])(X, Y)
    F2 = np.vectorize(system["f2"])(X, Y)

    plt.figure(figsize=(7, 6))
    c1 = plt.contour(X, Y, F1, levels=[0])
    c2 = plt.contour(X, Y, F2, levels=[0])
    if point is not None:
        plt.plot(point[0], point[1], "o", label=f"({point[0]:.4f}; {point[1]:.4f})")
        plt.legend()
    plt.xlim(x1, x2)
    plt.ylim(y1, y2)
    plt.grid(True)
    plt.title(f"График системы: x ∈ [{x1:.3f}; {x2:.3f}], y ∈ [{y1:.3f}; {y2:.3f}]")
    plt.show()


def bisection(f, a, b, eps, max_iter=1000):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None, 0, "На концах интервала нет смены знака"
    
    it = 0
    while abs(b - a) > eps and it < max_iter:
        x = (a + b) / 2
        fx = f(x)
        it += 1
        if fa * fx <= 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    return (a + b) / 2, it, None


def newton(f, df, x0, eps, max_iter=1000):
    x = x0
    for it in range(1, max_iter + 1):
        dfx = df(x)
        if abs(dfx) < 1e-12:
            return None, it - 1, "Производная слишком мала"
        
        x_next = x - f(x) / dfx
        if abs(x_next - x) < eps:
            return x_next, it, None
        
        x = x_next
    return None, max_iter, "Превышено число итераций"


def simple_iter_eq(f, df, a, b, eps, max_iter=1000):
    xs = np.linspace(a, b, 1000)
    m = max(abs(df(float(x))) for x in xs)
    if m == 0:
        return None, 0, "Не удалось выбрать lambda"
    
    lambd = -1 / m if df((a + b) / 2) > 0 else 1 / m
    q = max(abs(1 + lambd * df(float(x))) for x in xs)
    if q >= 1:
        return None, 0, f"Условие сходимости не выполнено: q = {q:.6f}"
    
    phi = lambda x: x + lambd * f(x)
    x = (a + b) / 2
    for it in range(1, max_iter + 1):
        x_next = phi(x)
        if abs(x_next - x) < eps:
            return x_next, it, None
        
        x = x_next
    return None, max_iter, "Превышено число итераций"


def convergence_q(system, x0, y0, d=0.2, samples=20):
    xs = np.linspace(x0 - d, x0 + d, samples)
    ys = np.linspace(y0 - d, y0 + d, samples)
    q = 0.0
    for x in xs:
        for y in ys:
            a = system["dphi"](float(x), float(y))
            q = max(q, abs(a[0][0]) + abs(a[0][1]), abs(a[1][0]) + abs(a[1][1]))
    return q


def simple_iter_sys(system, x0, y0, eps, max_iter=1000):
    q = convergence_q(system, x0, y0)
    if q >= 1:
        return None, None, 0, None, f"Условие сходимости не выполнено: q = {q:.6f}"
    
    x, y = x0, y0
    for it in range(1, max_iter + 1):
        x_next = system["phi1"](x, y)
        y_next = system["phi2"](x, y)
        dx, dy = abs(x_next - x), abs(y_next - y)
        if max(dx, dy) < eps:
            return x_next, y_next, it, (dx, dy), None
        
        x, y = x_next, y_next
    return None, None, max_iter, None, "Превышено число итераций"


def solve_equation(eq_num, method, a, b, eps):
    if eq_num not in EQUATIONS or method not in {1, 3, 5} or a >= b or eps <= 0:
        print("Неверные данные задачи")
        return
    
    eq = EQUATIONS[eq_num]
    roots = count_roots(eq["f"], a, b)
    if roots == 0:
        print("На интервале корней не найдено")
        plot_equation(eq, a, b)
        return
    
    if roots > 1:
        print("На интервале найдено несколько корней")
        plot_equation(eq, a, b)
        return

    if method == 1:
        root, it, err = bisection(eq["f"], a, b, eps)
        method_name = "половинного деления"
    elif method == 3:
        root, it, err = newton(eq["f"], eq["df"], (a + b) / 2, eps)
        method_name = "Ньютона"
    else:
        root, it, err = simple_iter_eq(eq["f"], eq["df"], a, b, eps)
        method_name = "простой итерации"

    if err:
        print(err)
        plot_equation(eq, a, b)
        return

    print("\nРезультат:")
    print(f"Уравнение: {eq['name']}")
    print(f"Метод: {method_name}")
    print(f"Корень: {root:.10f}")
    print(f"f(x): {eq['f'](root):.10f}")
    print(f"Итераций: {it}")
    plot_equation(eq, a, b, root)


def solve_system(sys_num, x0, y0, eps):
    if sys_num not in SYSTEMS or eps <= 0:
        print("Неверные данные задачи")
        return
    
    system = SYSTEMS[sys_num]
    x, y, it, errs, err = simple_iter_sys(system, x0, y0, eps)
    if err:
        print(err)
        plot_system(system)
        return

    print("\nРезультат:")
    print(f"Система: {system['name']}")
    print("Метод: простая итерация")
    print(f"x = {x:.10f}")
    print(f"y = {y:.10f}")
    print(f"Итераций: {it}")
    print(f"Вектор погрешностей: ({errs[0]:.10f}, {errs[1]:.10f})")
    print(f"Проверка f1(x, y) = {system['f1'](x, y):.10f}")
    print(f"Проверка f2(x, y) = {system['f2'](x, y):.10f}")
    plot_system(system, (x, y))


def keyboard_mode():
    task = ask_choice("\n1 — уравнение\n2 — система\nВаш выбор: ", {"1", "2"})

    if task == "1":
        print("\nДоступные уравнения:")
        for k, eq in EQUATIONS.items():
            print(f"{k} — {eq['name']}")
        eq_num = int(ask_choice("Выберите уравнение: ", {"1", "2", "3", "4"}))
        
        print("\nМетоды для варианта 2:")
        print("1 — метод половинного деления")
        print("3 — метод Ньютона")
        print("5 — метод простой итерации")
        method = int(ask_choice("Выберите метод: ", {"1", "3", "5"}))
        a, b = ask_interval()
        eps = ask_float("Введите точность eps: ", positive=True)
        solve_equation(eq_num, method, a, b, eps)
    else:
        print("\nДоступные системы:")
        for k, s in SYSTEMS.items():
            print(f"{k} — {s['name']}")
        sys_num = int(ask_choice("Выберите систему: ", {"1", "2"}))
        x0 = ask_float("Введите начальное приближение x0: ")
        y0 = ask_float("Введите начальное приближение y0: ")
        eps = ask_float("Введите точность eps: ", positive=True)
        solve_system(sys_num, x0, y0, eps)


def file_mode():
    while True:
        cfg = ask_config()
        task = cfg.get("type", "").lower()
        try:
            if task == "equation":
                solve_equation(int(cfg["number"]), int(cfg["method"]), float(cfg["a"]), float(cfg["b"]), float(cfg["eps"]))
                return
            
            if task == "system" and int(cfg.get("method", "7")) == 7:
                solve_system(int(cfg["number"]), float(cfg["x0"]), float(cfg["y0"]), float(cfg["eps"]))
                return
            
        except Exception:
            pass
        print("Введите путь заново.")


def main():
    mode = ask_choice("Выберите ввод:\n1 — клавиатура\n2 — файл\nВаш выбор: ", {"1", "2"})
    if mode == "1":
        keyboard_mode()
    else:
        file_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
