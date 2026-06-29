from pathlib import Path
import math
import pandas as pd
from scipy.stats import t


BASE_DIR = Path(__file__).resolve().parent
file_x = BASE_DIR / "variant_5_sample_X.csv"
file_y = BASE_DIR / "variant_5_sample_Y.csv"


data_x = pd.read_csv(file_x)
data_y = pd.read_csv(file_y)

x = data_x.iloc[:, 1]
y = data_y.iloc[:, 1]
alpha = 0.05
m = len(x)
n = len(y)


x_mean = x.mean()
y_mean = y.mean()

sx2 = x.var(ddof=1)
sy2 = y.var(ddof=1)

sp2 = ((m - 1) * sx2 + (n - 1) * sy2) / (m + n - 2)
sp = math.sqrt(sp2)

t_obs = (x_mean - y_mean) / (sp * math.sqrt(1 / m + 1 / n))
df = m + n - 2
t_crit = t.ppf(1 - alpha / 2, df)


print(f"Размер выборки X: m = {m}")
print(f"Размер выборки Y: n = {n}")
print(f"Уровень значимости: alpha = {alpha}")
print()

print("Выборочные характеристики:")
print(f"x̄ = {x_mean:.4f}")
print(f"ȳ = {y_mean:.4f}")
print(f"sx² = {sx2:.4f}")
print(f"sy² = {sy2:.4f}")
print()

print("Объединённая оценка дисперсии:")
print(f"sp² = {sp2:.4f}")
print(f"sp = {sp:.4f}")
print()

print("Статистика критерия:")
print(f"t_набл = {t_obs:.4f}")
print(f"t_кр = ±{t_crit:.4f}")
print(f"Число степеней свободы: {df}")
print()
