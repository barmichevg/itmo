from math import prod

EPS = 1e-24
def is_zero(x: float, eps: float = EPS) -> bool:
    return abs(x) <= eps


def fmt(x: float, digits: int = 20) -> str:
    if is_zero(x):
        x = 0.0
    return f"{x:.{digits}f}".rstrip("0").rstrip(".")


def ask_mode() -> str:
    while True:
        print("Выберите ввод: 1 — клавиатура, 2 — файл")
        mode = input("Ваш выбор (1/2): ").strip()
        if mode in ("1", "2"):
            return mode
        print("Ошибка: нужно ввести 1 или 2.\n")


def ask_n() -> int:
    while True:
        s = input("Введите n (<=20): ").strip()
        try:
            n = int(s)
            if 1 <= n <= 20:
                return n
            print("Ошибка: n должно быть от 1 до 20.\n")
        except ValueError:
            print("Ошибка: n должно быть целым числом.\n")


def read_from_keyboard():
    n = ask_n()

    A = [[0.0] * n for _ in range(n)]
    b = [0.0] * n

    print("Введите расширенную матрицу построчно (всего n+1 чисел в строке):")
    for i in range(n):
        while True:
            parts = input(f"Строка {i+1}: ").split()
            if len(parts) != n + 1:
                print(f"Ошибка: нужно {n+1} чисел. Повторите ввод строки.\n")
                continue
            try:
                row = list(map(float, parts))
            except ValueError:
                print("Ошибка: в строке должны быть только числа. Повторите ввод строки.\n")
                continue
            A[i] = row[:n]
            b[i] = row[n]
            break

    return A, b


def read_from_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            tokens = f.read().split()
    except FileNotFoundError:
        raise ValueError("Файл не найден.")

    if not tokens:
        raise ValueError("Файл пустой.")

    try:
        n = int(float(tokens[0]))
    except ValueError:
        raise ValueError("Первое значение в файле должно быть числом n.")

    if not (1 <= n <= 20):
        raise ValueError("n должно быть от 1 до 20.")

    need = 1 + n * (n + 1)
    if len(tokens) < need:
        raise ValueError(f"Недостаточно чисел в файле. Нужно {need}, есть {len(tokens)}.")

    A = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    idx = 1

    for i in range(n):
        chunk = tokens[idx: idx + n + 1]
        idx += n + 1
        try:
            row = list(map(float, chunk))
        except ValueError:
            raise ValueError(f"В файле в строке {i+1} есть нечисловые значения.")
        A[i] = row[:n]
        b[i] = row[n]

    return A, b


def print_augmented(U, c):
    n = len(U)
    print("\nМатрица после прямого хода (расширенная) [U|c]:")
    for i in range(n):
        left = "  ".join(fmt(U[i][j]) for j in range(n))
        print(f"{left} | {fmt(c[i])}")


def forward(A, b, eps: float = EPS):
    n = len(A)
    swaps = 0

    for i in range(n - 1):
        if is_zero(A[i][i], eps):
            p = -1
            for k in range(i + 1, n):
                if not is_zero(A[k][i], eps):
                    p = k
                    break
            if p != -1:
                A[i], A[p] = A[p], A[i]
                b[i], b[p] = b[p], b[i]
                swaps += 1

        if is_zero(A[i][i], eps):
            continue

        for k in range(i + 1, n):
            if is_zero(A[k][i], eps):
                continue
            c = A[k][i] / A[i][i]
            A[k][i] = 0.0
            for j in range(i + 1, n):
                A[k][j] -= c * A[i][j]
            b[k] -= c * b[i]

    return A, b, swaps


def classify(U, c, eps: float = EPS):
    n = len(U)
    rankA = 0
    rankAug = 0
    inconsistent = False

    for i in range(n):
        rowA_nonzero = any(abs(U[i][j]) >= eps for j in range(n))
        rowAug_nonzero = rowA_nonzero or (abs(c[i]) >= eps)

        if rowA_nonzero:
            rankA += 1
        if rowAug_nonzero:
            rankAug += 1
        if (not rowA_nonzero) and (abs(c[i]) >= eps):
            inconsistent = True

    if inconsistent or rankAug > rankA:
        return "NO_SOLUTIONS", rankA, rankAug
    if rankA < n:
        return "INFINITE_SOLUTIONS", rankA, rankAug
    return "UNIQUE_SOLUTION", rankA, rankAug


def reverse(U, c, eps: float = EPS):
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if is_zero(U[i][i], eps):
            raise ValueError("Диагональный элемент 0: невозможно получить единственное решение.")
        s = 0.0
        for j in range(i + 1, n):
            s += U[i][j] * x[j]
        x[i] = (c[i] - s) / U[i][i]
    return x


def residual(A0, b0, x):
    n = len(A0)
    r = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(n):
            s += A0[i][j] * x[j]
        r[i] = s - b0[i]
    return r


def main():
    try:
        mode = ask_mode()

        if mode == "1":
            A0, b0 = read_from_keyboard()
        else:
            path = input("Путь к файлу: ").strip()
            if not path:
                raise ValueError("Путь к файлу не задан.")
            A0, b0 = read_from_file(path)

        A = [row[:] for row in A0]
        b = b0[:]

        U, c, swaps = forward(A, b)
        print_augmented(U, c)

        status, rankA, rankAug = classify(U, c)

        det = prod(U[i][i] for i in range(len(U)))
        if swaps % 2 == 1:
            det = -det
        if status != "UNIQUE_SOLUTION":
            det = 0.0

        print(f"\nОпределитель det = {fmt(det)}")
        print(f"rank(A) = {rankA}, rank([A|b]) = {rankAug}")

        if status == "NO_SOLUTIONS":
            print("\nСИСТЕМА НЕ ИМЕЕТ РЕШЕНИЙ (несовместна).")
        elif status == "INFINITE_SOLUTIONS":
            print("\nСИСТЕМА ИМЕЕТ БЕСКОНЕЧНО МНОГО РЕШЕНИЙ (неопределённа).")
        else:
            print("\nСИСТЕМА ИМЕЕТ ЕДИНСТВЕННОЕ РЕШЕНИЕ.")
            try:
                x = reverse(U, c)
            except ValueError as e:
                print("\nОшибка обратного хода:", e)
                return

            print("\nВектор неизвестных x:")
            for i, xi in enumerate(x, 1):
                print(f"x{i} = {fmt(xi)}")

            r = residual(A0, b0, x)
            print("\nВектор невязок r = A*x - b:")
            for i, ri in enumerate(r, 1):
                print(f"r{i} = {fmt(ri)}")


        print("\n--- Сравнение с numpy ---")
        try:
            import numpy as np

            A_np = np.array(A0, dtype=float)
            b_np = np.array(b0, dtype=float)

            det_lib = float(np.linalg.det(A_np))
            print(f"det_lib (numpy) = {fmt(det_lib)}")

            if status == "UNIQUE_SOLUTION":
                x_lib = np.linalg.solve(A_np, b_np)
                print("\nРешение numpy (solve):")
                for i, xi in enumerate(x_lib, 1):
                    print(f"x{i}_lib = {fmt(float(xi))}")
            else:
                x_ls, *_ = np.linalg.lstsq(A_np, b_np, rcond=None)
                print("\nnumpy.solve неприменим.")
                print("Одно из возможных приближённых решений (lstsq):")
                for i, xi in enumerate(x_ls, 1):
                    print(f"x{i}_ls = {fmt(float(xi))}")

        except Exception as e:
            print("numpy: возникла ошибка:", e)

    except ValueError as e:
        print("\nОшибка:", e)


if __name__ == "__main__":
    main()