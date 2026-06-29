import math


FUNCTIONS = {
    1: "-3*x^3 - 5*x^2 + 4*x - 2",
    2: "x^3 - 1.89*x^2 - 2*x + 1.76",
    3: "x / (x^2 + 1)",
    4: "sin(x) + x^2",
    5: "1 / sqrt(x)",
    6: "1 / sqrt(1 - x)",
    7: "1 / sqrt(|x|)",
    8: "1 / x",
    9: "1 / sqrt(2*x - x^2)",
}

METHODS = {
    1: "Левые прямоугольники",
    2: "Правые прямоугольники",
    3: "Средние прямоугольники",
    4: "Трапеции",
    5: "Симпсон",
}

RUNGE_P = {1: 1, 2: 1, 3: 2, 4: 2, 5: 4}


def f(x, func_id):
    if func_id == 1:
        return -3 * x**3 - 5 * x**2 + 4 * x - 2
    if func_id == 2:
        return x**3 - 1.89 * x**2 - 2 * x + 1.76
    if func_id == 3:
        return x / (x**2 + 1)
    if func_id == 4:
        return math.sin(x) + x**2
    if func_id == 5:
        if x <= 0:
            raise ValueError
        return 1 / math.sqrt(x)
    if func_id == 6:
        if x >= 1:
            raise ValueError
        return 1 / math.sqrt(1 - x)
    if func_id == 7:
        if abs(x) <= 1e-10:
            raise ValueError
        return 1 / math.sqrt(abs(x))
    if func_id == 8:
        if abs(x) <= 1e-10:
            raise ValueError
        return 1 / x
    if func_id == 9:
        y = 2 * x - x * x
        if y <= 0:
            raise ValueError
        return 1 / math.sqrt(y)
    raise ValueError


def is_defined(func_id, x):
    try:
        y = f(x, func_id)
        return math.isfinite(y)
    except Exception:
        return False


def critical(func_id, x):
    if func_id in (1, 2, 3, 4):
        return None
    if func_id in (5, 7, 8):
        return x
    if func_id == 6:
        return 1 - x
    if func_id == 9:
        return 2 * x - x * x
    return None


def add_unique(points, x, tol=1e-7):
    for p in points:
        if abs(p - x) <= tol:
            return
    points.append(x)


def bisect_zero(func_id, a, b):
    g1 = critical(func_id, a)
    g2 = critical(func_id, b)

    for _ in range(60):
        m = (a + b) / 2
        gm = critical(func_id, m)

        if abs(gm) < 1e-12:
            return m
        if g1 * gm <= 0:
            b = m
            g2 = gm
        else:
            a = m
            g1 = gm

    return (a + b) / 2


def find_break_points(func_id, a, b, steps=2000):
    left, right = min(a, b), max(a, b)
    if critical(func_id, left) is None:
        return []

    points = []
    prev_x = left
    prev_g = critical(func_id, prev_x)

    if abs(prev_g) < 1e-10:
        add_unique(points, prev_x)

    for i in range(1, steps + 1):
        x = left + (right - left) * i / steps
        gx = critical(func_id, x)

        if abs(gx) < 1e-8:
            add_unique(points, x)
        elif prev_g * gx < 0:
            add_unique(points, bisect_zero(func_id, prev_x, x))

        prev_x = x
        prev_g = gx

    points.sort()
    return points


def split_segments(a, b, points):
    left, right = min(a, b), max(a, b)
    borders = [left] + points + [right]
    segments = []

    for i in range(len(borders) - 1):
        s, e = borders[i], borders[i + 1]
        if e - s > 1e-12:
            segments.append((s, e))

    return segments


def alpha_near_break(func_id, point, side, span):
    d = min(span / 4, 0.1)
    if d <= 1e-8:
        d = span / 10
    if d <= 1e-10:
        return 0.0

    x1 = point + side * d
    x2 = point + side * d / 2

    try:
        y1 = abs(f(x1, func_id))
        y2 = abs(f(x2, func_id))
    except Exception:
        return float("inf")

    if y1 <= 0 or y2 <= 0:
        return 0.0

    ratio = y2 / y1
    if ratio <= 1:
        return 0.0

    return math.log(ratio, 2)


def point_place(x, a, b):
    if abs(x - a) <= 1e-7:
        return "в точке a"
    if abs(x - b) <= 1e-7:
        return "в точке b"
    return "на отрезке интегрирования"


def analyze_function(func_id, a, b):
    points = find_break_points(func_id, a, b)
    segments = split_segments(a, b, points) if points else [(min(a, b), max(a, b))]

    valid_segments = []
    for s, e in segments:
        m = (s + e) / 2
        if is_defined(func_id, m):
            valid_segments.append((s, e))
        else:
            return {
                "ok": False,
                "reason": f"функция не определена на части интервала ({s:g}; {e:g})",
                "break_points": points,
                "segments": [],
            }

    for point in points:
        alphas = []

        for s, e in valid_segments:
            if abs(e - point) <= 1e-7:
                alphas.append(alpha_near_break(func_id, point, -1, e - s))
            if abs(s - point) <= 1e-7:
                alphas.append(alpha_near_break(func_id, point, 1, e - s))

        if alphas and max(alphas) >= 0.98:
            return {
                "ok": False,
                "reason": f"обнаружен бесконечный разрыв {point_place(point, a, b)}: x = {point:g}; интеграл расходится",
                "break_points": points,
                "segments": valid_segments,
            }

    return {
        "ok": True,
        "reason": "",
        "break_points": points,
        "segments": valid_segments,
    }


def left_rectangles(func_id, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h, func_id) for i in range(n))


def right_rectangles(func_id, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h, func_id) for i in range(1, n + 1))


def middle_rectangles(func_id, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h, func_id) for i in range(n))


def trapezoids(func_id, a, b, n):
    h = (b - a) / n
    s = (f(a, func_id) + f(b, func_id)) / 2
    for i in range(1, n):
        s += f(a + i * h, func_id)
    return h * s


def simpson(func_id, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    s = f(a, func_id) + f(b, func_id)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h, func_id)
    return h * s / 3


def integrate_once(func_id, method_id, a, b, n):
    if method_id == 1:
        return left_rectangles(func_id, a, b, n)
    if method_id == 2:
        return right_rectangles(func_id, a, b, n)
    if method_id == 3:
        return middle_rectangles(func_id, a, b, n)
    if method_id == 4:
        return trapezoids(func_id, a, b, n)
    return simpson(func_id, a, b, n)


def integrate_with_runge(func_id, method_id, a, b, eps):
    n = 4
    if method_id == 5 and n % 2 != 0:
        n += 1

    i1 = integrate_once(func_id, method_id, a, b, n)
    p = RUNGE_P[method_id]

    for _ in range(20):
        n2 = n * 2
        if method_id == 5 and n2 % 2 != 0:
            n2 += 1

        i2 = integrate_once(func_id, method_id, a, b, n2)
        error = abs(i2 - i1) / (2**p - 1)

        if error <= eps:
            return i2, n2

        n = n2
        i1 = i2

    raise ValueError("не удалось достичь требуемой точности")


def trim_segment(s, e, break_points, delta):
    left, right = s, e

    for p in break_points:
        if abs(s - p) <= 1e-7:
            left = s + delta
        if abs(e - p) <= 1e-7:
            right = e - delta

    if left >= right:
        return None
    return left, right


def integrate_improper(func_id, method_id, a, b, eps, segments, break_points):
    sign = -1 if a > b else 1
    base_segments = [(min(s, e), max(s, e)) for s, e in segments]

    min_len = min(e - s for s, e in base_segments)
    delta = min(min_len / 4, 0.1)
    if delta <= 1e-8:
        delta = min_len / 10

    prev_total = None

    for _ in range(20):
        total = 0.0
        total_n = 0
        part_eps = eps / max(1, 2 * len(base_segments))

        for s, e in base_segments:
            trimmed = trim_segment(s, e, break_points, delta)
            if trimmed is None:
                continue

            ta, tb = trimmed
            value, n = integrate_with_runge(func_id, method_id, ta, tb, part_eps)
            total += value
            total_n += n

        if prev_total is not None and abs(total - prev_total) <= eps / 2:
            return sign * total, total_n

        prev_total = total
        delta /= 2

    raise ValueError("не удалось вычислить несобственный интеграл")


def read_int(prompt, low, high):
    while True:
        try:
            x = int(input(prompt))
            if low <= x <= high:
                return x
            print("Ошибка. Введите число из списка.")
        except ValueError:
            print("Ошибка. Нужно ввести целое число.")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Ошибка. Нужно ввести число.")


def read_positive_float(prompt):
    while True:
        x = read_float(prompt)
        if x > 0:
            return x
        print("Ошибка. Точность должна быть больше нуля.")


def show_functions():
    print("Выберите функцию:")
    for i in range(1, 10):
        print(f"{i}. {FUNCTIONS[i]}")


def show_methods():
    print("\nВыберите метод:")
    for i in range(1, 6):
        print(f"{i}. {METHODS[i]}")


def main():
    show_functions()
    func_id = read_int("Номер функции: ", 1, 9)

    a = read_float("Нижний предел a: ")
    b = read_float("Верхний предел b: ")
    while abs(a - b) <= 1e-12:
        print("Ошибка. Пределы интегрирования не должны совпадать.")
        a = read_float("Нижний предел a: ")
        b = read_float("Верхний предел b: ")

    eps = read_positive_float("Точность eps: ")

    show_methods()
    method_id = read_int("Номер метода: ", 1, 5)

    info = analyze_function(func_id, a, b)

    print("\nРезультат:")

    if info["break_points"]:
        pts = ", ".join(f"{x:g}" for x in info["break_points"])
        print(f"Найдены точки разрыва: {pts}")

    if not info["ok"]:
        print("Интеграл не существует.")
        print("Причина:", info["reason"])
        return

    try:
        if info["break_points"]:
            result, n = integrate_improper(
                func_id, method_id, a, b, eps, info["segments"], info["break_points"]
            )
        else:
            result, n = integrate_with_runge(func_id, method_id, a, b, eps)

        print(f"Интеграл = {result}")
        print(f"Число разбиений n = {n}")
    except ValueError as e:
        print("Интеграл не удалось вычислить.")
        print("Причина:", e)


if __name__ == "__main__":
    main()