# fourier_all.py
# Fourier series: real form (a_n, b_n) and complex form (c_n)
# for 4 periodic functions with T=2 (your lab setup)

import os
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Parameters (your choice)
# ----------------------------
a = 1.0
b = 2.0
t0, t1, t2 = 1.0, 2.0, 3.0
T = t2 - t0  # 2.0

# Plot/compute settings
N_list_plots = [1, 2, 5, 10, 25]
N_parseval_list = [25, 50]
N_max = max(max(N_list_plots), max(N_parseval_list))
M = 20000  # integration grid points (midpoint rule); increase if you want more accuracy

OUTDIR = "fourier_plots"
os.makedirs(OUTDIR, exist_ok=True)

# ----------------------------
# Periodic helpers
# ----------------------------
def wrap_to_interval(t, left, T):
    """Map t to [left, left+T). Works for numpy arrays."""
    return ((t - left) % T) + left

# ----------------------------
# Functions f1..f4 (periodic)
# ----------------------------
def f1_square(t):
    """Square wave on [t0, t0+T)=[1,3): 1 on [1,2), 2 on [2,3), periodic with T=2."""
    tt = wrap_to_interval(np.asarray(t), t0, T)
    return np.where(tt < t1, a, b)

def f2_even(t):
    """Even periodic function: cos(pi t), period 2."""
    t = np.asarray(t)
    return np.cos(np.pi * t)

def f3_sawtooth(t):
    """Odd periodic sawtooth: f(t)=t on [-1,1), periodic with T=2."""
    t = np.asarray(t)
    tt = wrap_to_interval(t, -1.0, 2.0)  # to [-1, 1)
    return tt

def f4_neither(t):
    """Neither even nor odd, not only straight lines: sin(2pi t) + cos(pi t), period 2."""
    t = np.asarray(t)
    return np.sin(2.0*np.pi*t) + np.cos(np.pi*t)

FUNCTIONS = [
    ("f1_square", f1_square, t0),     # integrate over [1,3)
    ("f2_cos",    f2_even,   -1.0),   # integrate over [-1,1)
    ("f3_saw",    f3_sawtooth, -1.0), # integrate over [-1,1)
    ("f4_mix",    f4_neither, -1.0),  # integrate over [-1,1)
]

# ----------------------------
# Fourier coefficients by numeric integration (midpoint rule)
# ----------------------------
def fourier_coeffs_real(f, t_start, T, N, M=20000):
    """
    Compute a0, a[1..N], b[1..N] using midpoint rule on [t_start, t_start+T).
    """
    dt = T / M
    t = t_start + (np.arange(M) + 0.5) * dt
    y = f(t)

    a0 = (2.0 / T) * dt * np.sum(y)

    a = np.zeros(N + 1, dtype=float)  # a[0] unused (we keep a0 separately)
    b = np.zeros(N + 1, dtype=float)

    for n in range(1, N + 1):
        w = 2.0 * np.pi * n / T
        a[n] = (2.0 / T) * dt * np.sum(y * np.cos(w * t))
        b[n] = (2.0 / T) * dt * np.sum(y * np.sin(w * t))

    return a0, a, b

def real_to_complex(a0, a, b, N):
    """
    Convert real coefficients to complex coefficients c[-N..N].
    Uses:
      c0 = a0/2
      c_n = (a_n - i b_n)/2,  n>0
      c_-n = (a_n + i b_n)/2
    Returns array c with indices shifted: c[k+N] corresponds to c_k.
    """
    c = np.zeros(2*N + 1, dtype=complex)
    c[N] = a0 / 2.0
    for n in range(1, N + 1):
        c[N + n] = (a[n] - 1j*b[n]) / 2.0
        c[N - n] = (a[n] + 1j*b[n]) / 2.0
    return c

# ----------------------------
# Partial sums F_N and G_N
# ----------------------------
def F_partial(t, a0, a, b, T, N):
    t = np.asarray(t)
    res = np.full_like(t, a0/2.0, dtype=float)
    for n in range(1, N+1):
        w = 2.0*np.pi*n/T
        res += a[n]*np.cos(w*t) + b[n]*np.sin(w*t)
    return res

def G_partial(t, c, T, N):
    """
    c: array length 2Nmax+1 for -Nmax..Nmax, but we use only -N..N.
    Here assume c is exactly for -N..N (length 2N+1) OR we pass sliced.
    """
    t = np.asarray(t)
    k = np.arange(-N, N+1)
    w = 2.0*np.pi*k/T
    # sum over k: c_k * exp(i w_k t)
    # c is aligned: c[k+N]
    return np.sum(c[np.newaxis, :] * np.exp(1j * w[np.newaxis, :] * t[:, np.newaxis]), axis=1)

# ----------------------------
# Energies and Parseval checks
# ----------------------------
def energy_time_domain(f, t_start, T, M=20000):
    dt = T / M
    t = t_start + (np.arange(M) + 0.5) * dt
    y = f(t)
    return (1.0/T) * dt * np.sum(np.abs(y)**2)

def energy_from_ab(a0, a, b, N):
    return (a0*a0)/4.0 + 0.5*np.sum(a[1:N+1]**2 + b[1:N+1]**2)

def energy_from_c(c):
    return np.sum(np.abs(c)**2)

def energy_of_partial_sum_time(F_vals, T, M):
    dt = T / M
    return (1.0/T) * dt * np.sum(np.abs(F_vals)**2)

# ----------------------------
# Nice printing helpers
# ----------------------------
def fmt_complex(z, digits=12):
    re = np.round(z.real, digits)
    im = np.round(z.imag, digits)
    if abs(re) < 10**(-digits): re = 0.0
    if abs(im) < 10**(-digits): im = 0.0
    if im == 0.0:
        return f"{re:.{digits}g}"
    if re == 0.0:
        return f"{im:.{digits}g}j"
    sign = "+" if im >= 0 else "-"
    return f"{re:.{digits}g} {sign} {abs(im):.{digits}g}j"

# ----------------------------
# Main run
# ----------------------------
def main():
    print("Parameters:")
    print(f"a={a}, b={b}, t0={t0}, t1={t1}, t2={t2}, T={T}")
    print(f"N_max={N_max}, M={M}\n")

    # Compute and store coefficients up to N_max for each function
    coeffs = {}

    for name, f, t_start in FUNCTIONS:
        a0, aa, bb = fourier_coeffs_real(f, t_start, T, N_max, M=M)
        c = real_to_complex(a0, aa, bb, N_max)
        coeffs[name] = {
            "f": f,
            "t_start": t_start,
            "a0": a0,
            "a": aa,
            "b": bb,
            "c": c,
        }

    # Print coefficients for N=2 for each function
    print("=== Coefficients for N=2 ===")
    for name, _, _ in FUNCTIONS:
        a0 = coeffs[name]["a0"]
        aa = coeffs[name]["a"]
        bb = coeffs[name]["b"]
        cmax = coeffs[name]["c"]  # -Nmax..Nmax
        # take slice for -2..2 from -Nmax..Nmax array
        N2 = 2
        mid = N_max
        c2 = cmax[mid-N2: mid+N2+1]  # length 5

        print(f"\n{name}:")
        print(f"a0 = {a0:.12g}")
        print(f"a1 = {aa[1]:.12g}, a2 = {aa[2]:.12g}")
        print(f"b1 = {bb[1]:.12g}, b2 = {bb[2]:.12g}")
        print("c_-2..c_2:")
        labels = ["c_-2", "c_-1", "c_0", "c_1", "c_2"]
        for lab, val in zip(labels, c2):
            print(f"  {lab} = {fmt_complex(val)}")

    # Parseval tables for N=25 and N=50
    for Np in N_parseval_list:
        print(f"\n\n=== Parseval table for N={Np} ===")
        header = (
            "function | E(f) | E_N(ab) | diff | E_N(c) | diff | "
            "E(F_N) | E(F_N)-E_N(ab) | E(G_N) | E(G_N)-E_N(c)"
        )
        print(header)
        print("-"*len(header))

        for name, f, t_start in FUNCTIONS:
            a0 = coeffs[name]["a0"]
            aa = coeffs[name]["a"]
            bb = coeffs[name]["b"]
            cmax = coeffs[name]["c"]

            # energies
            E = energy_time_domain(f, t_start, T, M=M)

            EN_ab = energy_from_ab(a0, aa, bb, Np)

            # complex slice -Np..Np from -Nmax..Nmax
            mid = N_max
            cNp = cmax[mid-Np: mid+Np+1]
            EN_c = energy_from_c(cNp)

            # energy of partial sums in time domain
            dt = T / M
            t_grid = t_start + (np.arange(M) + 0.5) * dt

            Fvals = F_partial(t_grid, a0, aa, bb, T, Np)
            Gvals = G_partial(t_grid, cNp, T, Np)

            EF = energy_of_partial_sum_time(Fvals, T, M)
            EG = energy_of_partial_sum_time(Gvals, T, M)

            print(
                f"{name:9s} | "
                f"{E: .12f} | "
                f"{EN_ab: .12f} | "
                f"{(E-EN_ab): .12f} | "
                f"{EN_c: .12f} | "
                f"{(E-EN_c): .12f} | "
                f"{EF: .12f} | "
                f"{(EF-EN_ab): .3e} | "
                f"{EG: .12f} | "
                f"{(EG-EN_c): .3e}"
            )

    # Plots: for each function and each N in N_list_plots
    print(f"\n\nSaving plots to: {OUTDIR}/")
    for name, f, t_start in FUNCTIONS:
        # choose plot range: cover at least 2-3 periods
        if name == "f1_square":
            t_plot = np.linspace(t0 - T, t0 + 2*T, 3000)  # [-1,5] for your params
        else:
            t_plot = np.linspace(-3.0, 3.0, 3000)

        f_plot = f(t_plot)

        a0 = coeffs[name]["a0"]
        aa = coeffs[name]["a"]
        bb = coeffs[name]["b"]
        cmax = coeffs[name]["c"]

        for Np in N_list_plots:
            # slice complex coeffs -Np..Np
            mid = N_max
            cNp = cmax[mid-Np: mid+Np+1]

            Fp = F_partial(t_plot, a0, aa, bb, T, Np)
            Gp = G_partial(t_plot, cNp, T, Np).real  # should match Fp for real f

            plt.figure(figsize=(10, 4))
            plt.plot(t_plot, f_plot, label="f(t)", linewidth=2.0)
            plt.plot(t_plot, Fp, label=f"F_N(t), N={Np}", linewidth=1.4)
            plt.plot(t_plot, Gp, label=f"Re G_N(t), N={Np}", linewidth=1.2, linestyle="--")
            plt.grid(True, alpha=0.3)
            plt.xlabel("t")
            plt.ylabel("value")
            plt.title(f"{name}: f(t) vs Fourier partial sums (T={T}, N={Np})")
            plt.legend()

            fname = os.path.join(OUTDIR, f"{name}_N{Np}.png")
            plt.tight_layout()
            plt.savefig(fname, dpi=200)
            plt.close()

    print("Done.")

if __name__ == "__main__":
    main()
