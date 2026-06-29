import math

EPS = 0.0001
MAX_ITER = 1000
X0 = (-2.0, 4.0)
GRAD_STEP = 0.25


def f(x1, x2):
    return 2 * x1**2 + 2 * x1 * x2 + 3 * x2**2 - 12 * x1 - 6 * x2 + 18


def grad(x1, x2):
    df_dx1 = 4 * x1 + 2 * x2 - 12
    df_dx2 = 2 * x1 + 6 * x2 - 6
    return df_dx1, df_dx2


def norm(v):
    return math.hypot(v[0], v[1])


def h_mul(v):
    return 4 * v[0] + 2 * v[1], 2 * v[0] + 6 * v[1]


def print_history(title, history):
    print(title)
    print(f"{'k':>3} {'x1':>12} {'x2':>12} {'f(x)':>14} {'||grad||':>14} {'step':>14}")
    for row in history:
        k, x1, x2, fx, gnorm, step = row
        step_str = "-" if step is None else f"{step:.6f}"
        print(f"{k:>3} {x1:>12.6f} {x2:>12.6f} {fx:>14.6f} {gnorm:>14.6f} {step_str:>14}")
    print()


def coordinate_descent(x0, eps=EPS, max_iter=MAX_ITER):
    x1, x2 = x0
    import math

EPS = 0.0001
MAX_ITER = 1000
X0 = (-2.0, 4.0)
GRAD_STEP = 0.25


def f(x1, x2):
    return 2 * x1**2 + 2 * x1 * x2 + 3 * x2**2 - 12 * x1 - 6 * x2 + 18


def grad(x1, x2):
    df_dx1 = 4 * x1 + 2 * x2 - 12
    df_dx2 = 2 * x1 + 6 * x2 - 6
    return df_dx1, df_dx2


def norm(v):
    return math.hypot(v[0], v[1])


def h_mul(v):
    return 4 * v[0] + 2 * v[1], 2 * v[0] + 6 * v[1]


def print_history(title, history):
    print(title)
    print(f"{'k':>3} {'x1':>12} {'x2':>12} {'f(x)':>14} {'||grad||':>14} {'step':>14}")
    for row in history:
        k, x1, x2, fx, gnorm, step = row
        step_str = "-" if step is None else f"{step:.6f}"
        print(f"{k:>3} {x1:>12.6f} {x2:>12.6f} {fx:>14.6f} {gnorm:>14.6f} {step_str:>14}")
    print()


def golden_section_min(func, a, b, eps=EPS):
    phi = (1 + math.sqrt(5)) / 2

    x1 = b - (b - a) / phi
    x2 = a + (b - a) / phi
    f1 = func(x1)
    f2 = func(x2)

    while abs(b - a) > eps:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = b - (b - a) / phi
            f1 = func(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (b - a) / phi
            f2 = func(x2)

    return (a + b) / 2


def coordinate_descent(x0, eps=EPS, max_iter=MAX_ITER):
    x1, x2 = x0
    history = [(0, x1, x2, f(x1, x2), norm(grad(x1, x2)), None)]
    step = 0

    for _ in range(max_iter):
        prev_x1, prev_x2 = x1, x2

        x1 = golden_section_min(lambda t: f(t, x2), -10.0, 10.0, eps)
        step += 1
        history.append((step, x1, x2, f(x1, x2), norm(grad(x1, x2)), None))

        x2 = golden_section_min(lambda t: f(x1, t), -10.0, 10.0, eps)
        step += 1
        history.append((step, x1, x2, f(x1, x2), norm(grad(x1, x2)), None))

        move = norm((x1 - prev_x1, x2 - prev_x2))
        if move < eps or norm(grad(x1, x2)) < eps:
            break

    return (x1, x2), history


def gradient_descent(x0, step_size=GRAD_STEP, eps=EPS, max_iter=MAX_ITER):
    x1, x2 = x0
    history = [(0, x1, x2, f(x1, x2), norm(grad(x1, x2)), None)]

    for k in range(1, max_iter + 1):
        g1, g2 = grad(x1, x2)
        gnorm = norm((g1, g2))

        if gnorm < eps:
            break

        current_f = f(x1, x2)
        current_step = step_size

        while True:
            new_x1 = x1 - current_step * g1
            new_x2 = x2 - current_step * g2
            new_f = f(new_x1, new_x2)

            if new_f < current_f:
                break

            current_step /= 2


        x1, x2 = new_x1, new_x2
        history.append((k, x1, x2, new_f, norm(grad(x1, x2)), current_step))

    return (x1, x2), history


def steepest_descent(x0, eps=EPS, max_iter=MAX_ITER):
    x1, x2 = x0
    history = [(0, x1, x2, f(x1, x2), norm(grad(x1, x2)), None)]

    for k in range(1, max_iter + 1):
        g1, g2 = grad(x1, x2)
        gnorm = norm((g1, g2))

        if gnorm < eps:
            break

        s1 = g1 / gnorm
        s2 = g2 / gnorm

        phi = lambda lam: f(x1 + lam * s1, x2 + lam * s2)

        lam = golden_section_min(phi, -10.0, 10.0, eps)

        x1 = x1 + lam * s1
        x2 = x2 + lam * s2

        history.append((k, x1, x2, f(x1, x2), norm(grad(x1, x2)), lam))

    return (x1, x2), history


point_cd, hist_cd = coordinate_descent(X0)
point_gd, hist_gd = gradient_descent(X0)
point_sd, hist_sd = steepest_descent(X0)

print_history("Метод покоординатного спуска", hist_cd)
print(f"Итог: x = ({point_cd[0]:.6f}, {point_cd[1]:.6f}), f(x) = {f(*point_cd):.6f}")
print()

print_history("Метод градиентного спуска", hist_gd)
print(f"Итог: x = ({point_gd[0]:.6f}, {point_gd[1]:.6f}), f(x) = {f(*point_gd):.6f}")
print()

print_history("Метод наискорейшего спуска", hist_sd)
print(f"Итог: x = ({point_sd[0]:.6f}, {point_sd[1]:.6f}), f(x) = {f(*point_sd):.6f}")