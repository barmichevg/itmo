import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal

out_dir = os.path.dirname(__file__)
fig_dir = os.path.join(out_dir, "figs")
os.makedirs(fig_dir, exist_ok=True)

def unitary_fft(f, dt):
    F = (dt/np.sqrt(2*np.pi)) * np.fft.fft(f)
    w = 2*np.pi*np.fft.fftfreq(len(f), d=dt)
    return w, F

def unitary_ifft(F, dt):
    return (np.sqrt(2*np.pi)/dt) * np.fft.ifft(F)

def build_signal(t, a, t1, t2):
    return np.where((t>=t1) & (t<=t2), a, 0.0)

def pad_to_pow2(x, pad_factor=4):
    n = len(x)
    n_pad = 1 << int(np.ceil(np.log2(n*pad_factor)))
    y = np.zeros(n_pad, dtype=float)
    y[:n] = x
    return y, n_pad

def plot_time(t, g, u, y, y_ifft, title, fname, tlim=None):
    plt.figure(figsize=(10,4))
    plt.plot(t, g, label="g(t)")
    plt.plot(t, u, label="u(t)", alpha=0.7)
    plt.plot(t, y, label="y(t) time", linewidth=2)
    plt.plot(t, y_ifft, label="IFFT(W·Û)", linestyle="--", linewidth=2)
    if tlim:
        plt.xlim(*tlim)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, fname), dpi=180)
    plt.close()

def plot_spectrum(w, G, U, Y, WYU, title, fname, wmax=200):
    idx = (w>=0) & (w<=wmax)
    plt.figure(figsize=(10,4))
    plt.plot(w[idx], np.abs(G[idx]), label="|ĝ|")
    plt.plot(w[idx], np.abs(U[idx]), label="|û|", alpha=0.8)
    plt.plot(w[idx], np.abs(Y[idx]), label="|ŷ|", linewidth=2)
    plt.plot(w[idx], np.abs(WYU[idx]), label="|W·û|", linestyle="--", linewidth=2)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlabel("ω (рад/с)")
    plt.ylabel("модуль")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, fname), dpi=180)
    plt.close()

def plot_ach(w, W, title, fname, wmax=200):
    idx = (w>=0) & (w<=wmax)
    plt.figure(figsize=(8,4))
    plt.plot(w[idx], np.abs(W[idx]))
    plt.grid(True, alpha=0.3)
    plt.xlabel("ω (рад/с)")
    plt.ylabel("|W(iω)|")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, fname), dpi=180)
    plt.close()

# Настройки
dt = 0.001
L  = 10.0
t  = np.arange(0, L, dt)

a  = 1.0
t1 = 2.0
t2 = 4.0

# Часть 1: c=0
b_noise = 0.35
T_list = [0.02, 0.08, 0.25]

# Часть 2: b=0
w0 = 30.0
c_amp = 0.6
b1_list = [1.0, 6.0, 20.0]
d_list  = [0.8*w0, w0, 1.2*w0]

np.random.seed(7)

g = build_signal(t, a, t1, t2)



xi = np.random.uniform(-1, 1, size=len(t))
u1 = g + b_noise*xi

u_pad, _ = pad_to_pow2(u1)
w, _ = unitary_fft(u_pad, dt)
T_ach = 0.08
W1 = 1/(1+1j*w*T_ach)
plot_ach(w, W1, f"Часть 1: АЧХ W1, T={T_ach}", f"part1_ach_T{T_ach}.png", wmax=250)

for T in T_list:
    alpha = np.exp(-dt/T)
    y = np.zeros_like(u1)
    for n in range(1, len(u1)):
        y[n] = alpha*y[n-1] + (1-alpha)*u1[n]

    u_pad, _ = pad_to_pow2(u1)
    g_pad, _ = pad_to_pow2(g)
    y_pad, _ = pad_to_pow2(y)
    w, U = unitary_fft(u_pad, dt)
    _, G = unitary_fft(g_pad, dt)
    _, Y = unitary_fft(y_pad, dt)

    W1 = 1/(1+1j*w*T)
    WYU = W1*U
    y_ifft = np.real(unitary_ifft(WYU, dt))[:len(t)]

    plot_time(t, g, u1, y, y_ifft, f"Часть 1: T={T}", f"part1_time_T{T}.png", tlim=(0,6))
    plot_spectrum(w, G, U, Y, WYU, f"Часть 1: спектры, T={T}", f"part1_spectra_T{T}.png", wmax=250)



for b1 in b1_list:
    W2 = ((-w**2 + w0**2) / (-w**2 + 1j*b1*w + w0**2))
    plot_ach(w, W2, f"Часть 2: АЧХ W2, b1={b1}, ω0={w0}", f"part2_ach_b1{b1}.png", wmax=200)

b1 = 6.0
for d in d_list:
    u2 = g + c_amp*np.sin(d*t)
    num = [1.0, 0.0, w0**2]
    den = [1.0, b1, w0**2]
    bz, az, _ = signal.cont2discrete((num, den), dt, method='bilinear')
    bz = bz.flatten()
    y = signal.lfilter(bz, az, u2)

    u_pad, _ = pad_to_pow2(u2)
    g_pad, _ = pad_to_pow2(g)
    y_pad, _ = pad_to_pow2(y)
    w, U = unitary_fft(u_pad, dt)
    _, G = unitary_fft(g_pad, dt)
    _, Y = unitary_fft(y_pad, dt)

    W2 = ((-w**2 + w0**2) / (-w**2 + 1j*b1*w + w0**2))
    WYU = W2*U
    y_ifft = np.real(unitary_ifft(WYU, dt))[:len(t)]

    plot_time(t, g, u2, y, y_ifft, f"Часть 2: b1={b1}, d={d:.1f}", f"part2_time_b1{b1}_d{d:.1f}.png", tlim=(0,6))
    plot_spectrum(w, G, U, Y, WYU, f"Часть 2: спектры, b1={b1}, d={d:.1f}", f"part2_spectra_b1{b1}_d{d:.1f}.png", wmax=200)

print("Готово. Смотри картинки в папке:", fig_dir)
