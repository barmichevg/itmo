import pandas as pd
import numpy as np

df = pd.read_csv("SBER_221201_251201day.csv", sep=";")
df["Date"] = pd.to_datetime(df["<DATE>"].astype(str), format="%y%m%d")
df = df.sort_values("Date")
u = df["<CLOSE>"].astype(float).to_numpy()

def smooth_first_order(u, T_days, dt=1.0):
    alpha = np.exp(-dt / T_days)
    y = np.empty_like(u, dtype=float)
    y[0] = u[0]
    for n in range(1, len(u)):
        y[n] = alpha*y[n-1] + (1-alpha)*u[n]
    return y
