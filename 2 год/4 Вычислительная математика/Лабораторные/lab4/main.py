import math
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent


def read_points():
    while True:
        print("1 - ввод с клавиатуры")
        print("2 - ввод из файла")
        mode = input("Ваш выбор: ").strip()

        if mode not in ("1", "2"):
            print("Некорректный выбор. Введите 1 или 2.\n")
            continue

        points = []

        if mode == "2":
            while True:
                path_str = input("Введите путь к файлу: ").strip().strip('"')
                path = Path(path_str)

                if not path.is_absolute():
                    path = BASE_DIR / path

                if not path.exists():
                    print("Файл не найден. Попробуйте снова.\n")
                    continue

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        points = []
                        for line in f:
                            line = line.strip().replace(";", " ")
                            if not line or line.startswith("#"):
                                continue

                            parts = line.split()
                            if len(parts) != 2:
                                raise ValueError("Каждая строка файла должна содержать два числа: x y")

                            x, y = map(float, parts)
                            points.append((x, y))
                    break
                except Exception as e:
                    print("Ошибка чтения файла:", e)
                    print("Попробуйте снова.\n")

        else:
            while True:
                try:
                    n = int(input("Введите количество точек (6-12): "))
                    if not 6 <= n <= 12:
                        print("Количество точек должно быть от 6 до 12.\n")
                        continue
                    break
                except ValueError:
                    print("Введите целое число от 6 до 12.\n")

            for i in range(n):
                while True:
                    try:
                        raw = input(f"Точка {i + 1} (x y): ").strip().replace(";", " ")
                        parts = raw.split()

                        if len(parts) != 2:
                            print("Введите ровно два числа: x y")
                            continue

                        x, y = map(float, parts)
                        points.append((x, y))
                        break
                    except ValueError:
                        print("Некорректный ввод. Введите два числа, например: 1.2 3.4")

        if not 6 <= len(points) <= 12:
            print("Нужно 6-12 точек. Введите данные заново.\n")
            continue

        xs = [p[0] for p in points]
        if len(set(xs)) != len(xs):
            print("Значения x не должны повторяться. Введите данные заново.\n")
            continue

        points.sort()
        return np.array([p[0] for p in points], dtype=float), np.array([p[1] for p in points], dtype=float)


def metrics(y, y_fit):
    s = float(np.sum((y_fit - y) ** 2))
    sigma = math.sqrt(s / len(y))
    y_mean = float(np.mean(y))
    ss_tot = float(np.sum((y - y_mean) ** 2))
    r2 = 1 - s / ss_tot if ss_tot != 0 else 1.0
    return s, sigma, r2


def pearson(x, y):
    x_mean = float(np.mean(x))
    y_mean = float(np.mean(y))
    num = float(np.sum((x - x_mean) * (y - y_mean)))
    den = math.sqrt(float(np.sum((x - x_mean) ** 2) * np.sum((y - y_mean) ** 2)))
    return num / den if den != 0 else 0.0


def poly_fit(x, y, deg, name):
    coeffs = np.polyfit(x, y, deg)
    p = np.poly1d(coeffs)
    y_fit = p(x)
    s, sigma, r2 = metrics(y, y_fit)

    if deg == 1:
        formula = f"y = {coeffs[0]:.6f}*x + {coeffs[1]:.6f}"
    elif deg == 2:
        formula = f"y = {coeffs[0]:.6f}*x^2 + {coeffs[1]:.6f}*x + {coeffs[2]:.6f}"
    else:
        formula = (
            f"y = {coeffs[0]:.6f}*x^3 + {coeffs[1]:.6f}*x^2 + "
            f"{coeffs[2]:.6f}*x + {coeffs[3]:.6f}"
        )

    result = {
        "name": name,
        "formula": formula,
        "coeffs": coeffs,
        "predict": lambda t: p(t),
        "S": s,
        "sigma": sigma,
        "R2": r2,
        "ok": True,
    }

    if deg == 1:
        result["pearson"] = pearson(x, y)

    return result


def exp_fit(x, y):
    if np.any(y <= 0):
        return {
            "name": "Экспоненциальная функция",
            "formula": "y = a*e^(b*x)",
            "ok": False,
            "reason": "нужны только y > 0",
        }

    coeffs = np.polyfit(x, np.log(y), 1)
    b, ln_a = coeffs[0], coeffs[1]
    a = math.exp(ln_a)

    predict = lambda t: a * np.exp(b * t)
    y_fit = predict(x)
    s, sigma, r2 = metrics(y, y_fit)

    return {
        "name": "Экспоненциальная функция",
        "formula": f"y = {a:.6f}*e^({b:.6f}*x)",
        "coeffs": [a, b],
        "predict": predict,
        "S": s,
        "sigma": sigma,
        "R2": r2,
        "ok": True,
    }


def log_fit(x, y):
    if np.any(x <= 0):
        return {
            "name": "Логарифмическая функция",
            "formula": "y = a*ln(x) + b",
            "ok": False,
            "reason": "нужны только x > 0",
        }

    coeffs = np.polyfit(np.log(x), y, 1)
    a, b = coeffs[0], coeffs[1]

    predict = lambda t: a * np.log(t) + b
    y_fit = predict(x)
    s, sigma, r2 = metrics(y, y_fit)

    return {
        "name": "Логарифмическая функция",
        "formula": f"y = {a:.6f}*ln(x) + {b:.6f}",
        "coeffs": [a, b],
        "predict": predict,
        "S": s,
        "sigma": sigma,
        "R2": r2,
        "ok": True,
    }


def power_fit(x, y):
    if np.any(x <= 0) or np.any(y <= 0):
        return {
            "name": "Степенная функция",
            "formula": "y = a*x^b",
            "ok": False,
            "reason": "нужны x > 0 и y > 0",
        }

    coeffs = np.polyfit(np.log(x), np.log(y), 1)
    b, ln_a = coeffs[0], coeffs[1]
    a = math.exp(ln_a)

    predict = lambda t: a * (t ** b)
    y_fit = predict(x)
    s, sigma, r2 = metrics(y, y_fit)

    return {
        "name": "Степенная функция",
        "formula": f"y = {a:.6f}*x^{b:.6f}",
        "coeffs": [a, b],
        "predict": predict,
        "S": s,
        "sigma": sigma,
        "R2": r2,
        "ok": True,
    }


def build_text(results, best):
    lines = ["Аппроксимация методом наименьших квадратов", ""]

    for r in results:
        lines.append(r["name"] + ":")
        lines.append("  " + r["formula"])

        if not r["ok"]:
            lines.append("  Недоступно: " + r["reason"])
            lines.append("")
            continue

        lines.append("  Коэффициенты: " + str([round(float(c), 6) for c in r["coeffs"]]))
        lines.append(f"  S = {r['S']:.6f}")
        lines.append(f"  sigma = {r['sigma']:.6f}")
        lines.append(f"  R^2 = {r['R2']:.6f}")

        if "pearson" in r:
            lines.append(f"  r = {r['pearson']:.6f}")

        lines.append("")

    lines.append("Лучшая функция: " + best["name"])
    lines.append(best["formula"])
    lines.append(f"sigma = {best['sigma']:.6f}")

    return "\n".join(lines)


def plot_all(x, y, results, best):
    x_min, x_max = float(np.min(x)), float(np.max(x))
    dx = x_max - x_min if x_max != x_min else 1.0

    left = x_min - 0.1 * dx
    right = x_max + 0.1 * dx
    grid = np.linspace(left, right, 500)

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, label="Точки")

    y_all = list(y)

    for r in results:
        if not r["ok"]:
            continue

        try:
            with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
                yg = r["predict"](grid)

            yg = np.array(yg, dtype=float)
            mask = np.isfinite(yg)

            if np.any(mask):
                plt.plot(
                    grid[mask],
                    yg[mask],
                    label=r["name"] + (" (лучшая)" if r["name"] == best["name"] else "")
                )
                y_all.extend(list(yg[mask]))
        except Exception:
            pass

    y_min, y_max = min(y_all), max(y_all)
    dy = y_max - y_min if y_max != y_min else 1.0

    plt.xlim(left, right)
    plt.ylim(y_min - 0.1 * dy, y_max + 0.1 * dy)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Аппроксимация функции")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plot_path = BASE_DIR / "plot.png"
    plt.savefig(plot_path, dpi=200)
    plt.show()


def main():
    x, y = read_points()

    results = [
        poly_fit(x, y, 1, "Линейная функция"),
        poly_fit(x, y, 2, "Полиномиальная 2-й степени"),
        poly_fit(x, y, 3, "Полиномиальная 3-й степени"),
        exp_fit(x, y),
        log_fit(x, y),
        power_fit(x, y),
    ]

    valid = [r for r in results if r["ok"]]
    best = min(valid, key=lambda r: r["sigma"])
    text = build_text(results, best)

    while True:
        print("\n1 - вывести в консоль")
        print("2 - сохранить в файл")
        out_mode = input("Ваш выбор: ").strip()

        if out_mode in ("1", "2"):
            break

        print("Некорректный выбор. Введите 1 или 2.\n")

    if out_mode == "2":
        result_path = BASE_DIR / "result.txt"
        with open(result_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Результаты сохранены в {result_path}")
    else:
        print("\n" + text)

    plot_all(x, y, results, best)
    print(f"График сохранен в {BASE_DIR / 'plot.png'}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Ошибка:", e)