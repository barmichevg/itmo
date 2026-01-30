import numpy as np
import matplotlib.pyplot as plt

def julia_set(c, xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width, dtype=np.float64)
    y = np.linspace(ymin, ymax, height, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    iters = np.zeros(Z.shape, dtype=np.uint16)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        Z[mask] = Z[mask] * Z[mask] + c
        escaped = np.abs(Z) > 2.0
        just_escaped = escaped & mask
        iters[just_escaped] = i
        mask &= ~escaped
        if not mask.any():
            break

    iters[mask] = max_iter
    return iters

def render_show(iters, bounds, title):
    xmin, xmax, ymin, ymax = bounds
    plt.figure()
    plt.imshow(iters, extent=[xmin, xmax, ymin, ymax], origin="lower", interpolation="nearest")
    plt.title(title)
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    plt.tight_layout()
    plt.show()

# Параметры визуализации
bounds = (-1.6, 1.6, -1.6, 1.6)
width, height = 900, 600

# Параметры C
c_list = [
    complex(-0.5251993, 0.5251993),
    complex(0.285, 0.0125),
    complex(-0.182, -0.666),
]

# Кол-во итераций
iteration_counts = [15, 50, 250]
for c in c_list:
    for n in iteration_counts:
        # Общий вид
        it = julia_set(c, *bounds, width=width, height=height, max_iter=n)
        render_show(it, bounds, f"Множество Жюлиа: c={c.real:+}; {c.imag:+}i ({n} итераций)")
