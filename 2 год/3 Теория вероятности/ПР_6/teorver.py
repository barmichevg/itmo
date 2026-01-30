import numpy as np
import math

X = np.array([750, 1250, 1750, 2250, 2750, 3250], dtype=float)
Y = np.array([15, 30, 45, 60, 75, 90, 105, 120], dtype=float)
m = np.array([
    [2, 4, 2, 0, 0, 0, 0, 0],
    [0, 0, 6, 7, 3, 0, 0, 0],
    [0, 0, 0, 6, 13, 9, 0, 0],
    [0, 0, 0, 6, 8, 9, 0, 0],
    [0, 0, 0, 0, 7, 8, 1, 0],
    [0, 0, 0, 0, 0, 1, 5, 3]
], dtype=float)

n = m.sum()
mx = m.sum(axis=1)
my = m.sum(axis=0)
x_mean = (mx * X).sum() / n
y_mean = (my * Y).sum() / n
sum_mx_x2 = (mx * X**2).sum()
sum_my_y2 = (my * Y**2).sum()
sum_mx_x  = (mx * X).sum()
sum_my_y  = (my * Y).sum()
sx2 = (sum_mx_x2 - (sum_mx_x**2) / n) / (n - 1)
sy2 = (sum_my_y2 - (sum_my_y**2) / n) / (n - 1)

sx = math.sqrt(sx2)
sy = math.sqrt(sy2)

cross_sum = 0.0
for i in range(len(X)):
    for j in range(len(Y)):
        cross_sum += m[i, j] * X[i] * Y[j]

sxy = (cross_sum - (sum_mx_x * sum_my_y) / n) / (n - 1)
r = sxy / (sx * sy)

a = r * sy / sx
b = y_mean - a * x_mean

print("x̄ =", x_mean)
print("ȳ =", y_mean)
print("sx =", sx)
print("sy =", sy)
print("sxy =", sxy)
print("r_xy =", r)
print(f"y = {b:.2f} + {a:.5f} x")
