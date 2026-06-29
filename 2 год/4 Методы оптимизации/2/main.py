import numpy as np
import matplotlib.pyplot as plt

# функция и производные
def f(x):
    return np.sin(x)**3 + np.cos(x)**2 - 0.5*np.sin(2*x)

def fp(x):
    return 3*np.sin(x)**2*np.cos(x) - np.sin(2*x) - np.cos(2*x)

def fpp(x):
    return (6*np.sin(x)*np.cos(x)**2 - 3*np.sin(x)**3 - 2*np.cos(2*x) + 2*np.sin(2*x))


# корень уравнения F(x)=0 на отрезке [a,b]
def bisection_root(F, a, b, tol=1e-12, max_iter=200):
    fa, fb = F(a), F(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        return None

    for _ in range(max_iter):
        c = 0.5*(a + b)
        fc = F(c)
        if abs(fc) < tol or (b - a)/2 < tol:
            return c
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return 0.5*(a + b)


# все стационарные точки на [A,B]
def find_stationary_points(A, B, N=20000):
    xs = np.linspace(A, B, N+1)
    ys = fp(xs)

    roots = []
    for i in range(N):
        x1, x2 = xs[i], xs[i+1]
        y1, y2 = ys[i], ys[i+1]

        if abs(y1) < 1e-10:
            roots.append(x1)

        if y1 * y2 < 0:
            r = bisection_root(fp, x1, x2)
            if r is not None:
                roots.append(r)

    roots = sorted(roots)
    unique = []
    for r in roots:
        if not unique or abs(r - unique[-1]) > 1e-6:
            unique.append(r)
    return np.array(unique)


# метод половинного деления
def dichotomy_minimize(func, a, b, eps=5e-5):
    delta = eps/2
    it = 0
    while (b - a) > 2*eps:
        c = 0.5*(a + b)
        x1 = c - delta
        x2 = c + delta
        if func(x1) > func(x2):
            a = c
        else:
            b = c
        it += 1
    return 0.5*(a + b), it

# метод золотого сечения
def golden_section_minimize(func, a, b, eps=5e-5):
    phi = (1 + np.sqrt(5)) / 2
    alpha = 1 - 1/phi
    beta  = 1/phi

    x1 = a + alpha*(b - a)
    x2 = a + beta*(b - a)
    f1 = func(x1)
    f2 = func(x2)

    it = 0
    while (b - a) > 2*eps:
        if f1 > f2:
            a = x1
            x1, f1 = x2, f2
            x2 = a + beta*(b - a)
            f2 = func(x2)
        else:
            b = x2
            x2, f2 = x1, f1
            x1 = a + alpha*(b - a)
            f1 = func(x1)
        it += 1

    return 0.5*(a + b), it

# метод хорд
def chord_root(F, a, b, eps=5e-5, max_iter=500):
    fa, fb = F(a), F(b)
    if fa * fb > 0:
        return None, 0

    x_prev = None
    for it in range(1, max_iter+1):
        x = (a*fb - b*fa) / (fb - fa)
        fx = F(x)

        if x_prev is not None and abs(x - x_prev) <= eps:
            return x, it
        x_prev = x

        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx

    return x, max_iter

# метод Ньютона
def newton_root_hybrid(F, Fp, a, b, eps=5e-5, max_iter=50):
    x = 0.5*(a + b)
    fa, fb = F(a), F(b)
    if fa * fb > 0:
        return None, 0

    for it in range(1, max_iter+1):
        fx = F(x)
        fpx = Fp(x)

        if fpx != 0:
            x_new = x - fx / fpx
        else:
            x_new = 0.5*(a + b)

        if (x_new < a) or (x_new > b) or (not np.isfinite(x_new)):
            x_new = 0.5*(a + b)

        if abs(x_new - x) <= eps:
            return x_new, it

        fx_new = F(x_new)
        if fa * fx_new < 0:
            b, fb = x_new, fx_new
        else:
            a, fa = x_new, fx_new

        x = x_new

    return x, max_iter



def main():
    A, B = -5.0, 3.0
    eps = 5e-5

    stat = find_stationary_points(A, B, N=30000)

    bounds = [A]
    for i in range(len(stat)-1):
        bounds.append(0.5*(stat[i] + stat[i+1]))
    bounds.append(B)

    print("f(x) = sin^3(x) + cos^2(x) - 0.5 sin(2x)")
    print(f"Отрезок: [{A}, {B}]")
    print("\nВнутренние экстремумы (корни f'(x)=0):")
    print("тип   x*        f(x*)     пол.дел.  зол.сеч.  хорды     Ньютон")

    mins = 0
    maxs = 0

    for i, x0 in enumerate(stat):
        a, b = bounds[i], bounds[i+1]

        t = "min" if fpp(x0) > 0 else "max"
        if t == "min":
            mins += 1
            func_opt = f
        else:
            maxs += 1
            func_opt = lambda x: -f(x)

        x_d, _ = dichotomy_minimize(func_opt, a, b, eps=eps)
        x_g, _ = golden_section_minimize(func_opt, a, b, eps=eps)
        x_c, _ = chord_root(fp, a, b, eps=eps)
        x_n, _ = newton_root_hybrid(fp, fpp, a, b, eps=eps)

        print(f"{t:3s}  {x0:8.4f}  {f(x0):8.4f}  "
              f"{x_d:8.4f}  {x_g:8.4f}  {x_c:8.4f}  {x_n:8.4f}")

    h = 1e-4
    left_type  = "min" if f(A) <= f(A + h) else "max"
    right_type = "min" if f(B) <= f(B - h) else "max"

    print("\nКоличество экстремумов:")
    print(f"Внутренние: min = {mins}, max = {maxs}")

    xs = np.linspace(A, B, 4000)

    # f(x)
    plt.figure()
    plt.plot(xs, f(xs))
    plt.scatter(stat, f(stat), marker="o", label="внутренние экстремумы")
    plt.scatter([A, B], [f(A), f(B)], marker="s", label="концы отрезка")
    plt.title("f(x) на [-5, 3]")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()

    # f'(x)
    plt.figure()
    plt.plot(xs, fp(xs))
    plt.axhline(0)
    plt.scatter(stat, fp(stat), marker="o")
    plt.title("f'(x) на [-5, 3] (нули = стационарные точки)")
    plt.xlabel("x")
    plt.ylabel("f'(x)")
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    main()