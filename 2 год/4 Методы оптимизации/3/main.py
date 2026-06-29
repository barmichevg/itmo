import math


def f(x):
    return x**2 - 3*x + x * math.log(x)


def quadratic_point(x1, x2, x3):
    f1 = f(x1)
    f2 = f(x2)
    f3 = f(x3)

    num = (x2**2 - x3**2) * f1 + (x3**2 - x1**2) * f2 + (x1**2 - x2**2) * f3
    den = 2 * ((x2 - x3) * f1 + (x3 - x1) * f2 + (x1 - x2) * f3)

    if abs(den) < 1e-24:
        return None

    return num / den


def quadratic_approximation(
        x1=1.25, 
        dx=0.05, 
        eps=0.0001, 
        max_iter=100
        ):
    print( f"{'k':>2} | {'x1':>9} | {'x2':>9} | {'x3':>9} | {'x_min':>9} | {'x_bar':>9} | {'f(x_bar)':>12}" )
    print("-" * 80)

    for k in range(1, max_iter + 1):
        x2 = x1 + dx

        f1 = f(x1)
        f2 = f(x2)

        if f1 > f2: x3 = x1 + 2 * dx
        else: x3 = x1 - dx


        f3 = f(x3)

        points = [(x1, f1), (x2, f2), (x3, f3)]
        points.sort(key=lambda p: p[0])

        x1, f1 = points[0]
        x2, f2 = points[1]
        x3, f3 = points[2]


        x_min, F_min = min(points, key=lambda p: p[1])


        x_bar = quadratic_point(x1, x2, x3)
        if x_bar is None:
            print( f"{k:2d} | {x1:9.6f} | {x2:9.6f} | {x3:9.6f} | {x_min:9.6f} | {'-':>9} | {'-':>12} | {'-':>10} | {'-':>10} | {'den=0, x1=x_min':>16}" )
            x1 = x_min
            continue
        f_bar = f(x_bar)


        print( f"{k:2d} | {x1:9.6f} | {x2:9.6f} | {x3:9.6f} | {x_min:9.6f} | {x_bar:9.6f} | {f_bar:12.6f}" )


        A = abs((F_min - f_bar) / f_bar)
        B = abs((x_min - x_bar) / x_bar)

        if A < eps and B < eps:
            return x_bar, f_bar

        if x1 <= x_bar <= x3:
            all_points = [(x1, f1), (x2, f2), (x3, f3), (x_bar, f_bar)]
            all_points.sort(key=lambda p: p[0])

            if F_min < f_bar:
                best_x = x_min
                best_f = F_min
            else:
                best_x = x_bar
                best_f = f_bar

            best_index = None
            for i, (x, fx) in enumerate(all_points):
                if abs(x - best_x) < 1e-24 and abs(fx - best_f) < 1e-24:
                    best_index = i
                    break

            if best_index == 0:
                new_points = all_points[:3]
            elif best_index == len(all_points) - 1:
                new_points = all_points[-3:]
            else:
                new_points = all_points[best_index - 1:best_index + 2]

            x1 = new_points[0][0]
            x2 = new_points[1][0]
            x3 = new_points[2][0]

            dx = x2 - x1

        else:
            x1 = x_bar

    return x_bar, f_bar

x_min, f_min = quadratic_approximation()

print("\nОтвет:")
print(f"x* = {x_min:.6f}")
print(f"f(x*) = {f_min:.6f}")