import numpy as np
import matplotlib.pyplot as plt

bin_edges = np.array([15, 32, 49, 66, 82, 99, 116, 133, 150, 167])
freq = np.array([68, 25, 17, 3, 4, 2, 0, 0, 1])

mid = (bin_edges[:-1] + bin_edges[1:]) / 2
n = freq.sum()

x_bar = np.sum(freq * mid) / n
s2 = np.sum(freq * (mid - x_bar)**2) / (n - 1) 
s = np.sqrt(s2)

print("n =", n)
print("x̄ ≈", x_bar)
print("s² ≈", s2)
print("s ≈", s)
print("[x̄-s, x̄+s] ≈", (x_bar - s, x_bar + s))


plt.figure(figsize=(12,4))
plt.hist(
    np.repeat(mid, freq),
    bins=bin_edges,
    edgecolor="black",
    alpha=0.7
)

plt.axvline(x_bar, linestyle="--", linewidth=2, label=f"Среднее ≈ {x_bar:.1f}")


plt.axvspan(x_bar - s, x_bar + s, alpha=0.15, label=f"[x̄−s, x̄+s] ≈ [{x_bar-s:.1f}, {x_bar+s:.1f}]")

plt.xlabel("Значение признака")
plt.ylabel("Частота")
plt.legend()
plt.grid(alpha=0.3)
plt.show()