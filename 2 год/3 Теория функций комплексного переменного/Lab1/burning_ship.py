import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def burning_ship_set(xmin, xmax, ymin, ymax, width, height, max_iter, supersample=2):
    sw, sh = width * supersample, height * supersample
    x = np.linspace(xmin, xmax, sw, dtype=np.float64)
    y = np.linspace(ymin, ymax, sh, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    Z = np.zeros_like(C, dtype=np.complex128)
    smooth = np.zeros(C.shape, dtype=np.float32)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(1, max_iter + 1):
        if not mask.any():
            break
        m = mask

        Zm = Z[m]
        Cr = C.real[m]
        Ci = C.imag[m]

        Zr = np.abs(Zm.real)
        Zi = np.abs(Zm.imag)

        Z_real = Zr*Zr - Zi*Zi + Cr
        Z_imag = 2.0 * Zr * Zi + Ci
        Z[m] = Z_real + 1j * Z_imag

        absZ = np.hypot(Z_real, Z_imag)
        esc_m = absZ > 2.0
        if np.any(esc_m):
            nu = i + 1.0 - np.log2(np.log(absZ[esc_m]))
            write = np.zeros_like(m, dtype=bool)
            write[m] = esc_m
            smooth[write] = nu.astype(np.float32)
            mask[write] = False

    smooth[mask] = float(max_iter)

    if supersample > 1:
        smooth = smooth.reshape(height, supersample, width, supersample).mean(axis=(1, 3))

    return smooth

def hist_normalize(field, max_iter):

    f = field.copy().ravel()
    inside = (f >= max_iter - 1e-6)
    g = f[~inside]
    if g.size > 0:

        order = np.argsort(g)
        ranks = np.empty_like(order, dtype=np.float64)
        ranks[order] = np.linspace(0.0, 1.0, num=g.size, endpoint=False)
        f[~inside] = ranks
    f[inside] = 0.0
    return f.reshape(field.shape).astype(np.float32)

def render_show(iters_like, bounds, title, zoom_rect=None, cmap="magma", flip_y=False, hist_norm=False, max_iter_for_norm=1000):
    img = iters_like
    if hist_norm:
        img = hist_normalize(img, max_iter_for_norm)

    xmin, xmax, ymin, ymax = bounds
    extent = [xmin, xmax, ymin, ymax]

    if flip_y:
        img = img[::-1, :]
        extent = [xmin, xmax, ymax, ymin]

    plt.figure()
    plt.imshow(img, extent=extent, origin="lower", interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    ax = plt.gca()
    if zoom_rect is not None:
        zxmin, zxmax, zymin, zymax = zoom_rect
        if flip_y:

            zymin, zymax = zymax, zymin
        rect = Rectangle((zxmin, zymin), zxmax-zxmin, zymax-zymin, fill=False, linewidth=1.0)
        ax.add_patch(rect)
    plt.tight_layout()
    plt.show()


# Параметры визуализации
width, height = 1400, 1000
zoom_bounds = (-1.82, -1.68, -0.08, 0.03)

# Кол-во итераций
for n in [50,100,500]:
    it_zoom = burning_ship_set(*zoom_bounds, width=width, height=height, max_iter=n, supersample=3)
    render_show(it_zoom, zoom_bounds,
                f"Горящий корабль: ({n} итераций)",
                hist_norm=True, max_iter_for_norm=n, flip_y=True, cmap="inferno")