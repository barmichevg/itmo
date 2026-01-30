import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width, dtype=np.float64)
    y = np.linspace(ymin, ymax, height, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C, dtype=np.complex128)
    iters = np.zeros(C.shape, dtype=np.uint16)
    mask = np.ones(C.shape, dtype=bool)
    for i in range(1, max_iter + 1):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        escaped = np.abs(Z) > 2.0
        just_escaped = escaped & mask
        iters[just_escaped] = i
        mask &= ~escaped
        if not mask.any():
            break

    iters[mask] = max_iter
    return iters

def render_show(iters, bounds, title, zoom_rect=None):
    xmin, xmax, ymin, ymax = bounds
    plt.figure()
    plt.imshow(iters, extent=[xmin, xmax, ymin, ymax], origin="lower", interpolation="nearest")
    plt.title(title)
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    ax = plt.gca()
    if zoom_rect is not None:
        zxmin, zxmax, zymin, zymax = zoom_rect
        rect = Rectangle((zxmin, zymin), zxmax-zxmin, zymax-zymin, fill=False, linewidth=1.5)
        ax.add_patch(rect)
    plt.tight_layout()
    plt.show()

# Параметры визуализации
bounds = (-2.5, 1.0, -1.25, 1.25)
width, height = 900, 600

# Область для приближения
zoom_center = (0.43, 0.35)
zoom_half_width = 0.06
zoom_half_height = 0.04
zoom_bounds = (
    zoom_center[0] - zoom_half_width,
    zoom_center[0] + zoom_half_width,
    zoom_center[1] - zoom_half_height,
    zoom_center[1] + zoom_half_height,
)

# Кол-во итераций
for n in [15, 50, 250]:
    # Общий вид
    it_full = mandelbrot_set(*bounds, width=width, height=height, max_iter=n)
    render_show(it_full, bounds, f"Множество Мандельброта — общий вид ({n} итераций)", zoom_rect=zoom_bounds)
    # Приближение
    it_zoom = mandelbrot_set(*zoom_bounds, width=width, height=height, max_iter=n)
    render_show(it_zoom, zoom_bounds, f"Множество Мандельброта — приближение ({n} итераций)")
