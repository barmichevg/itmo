from pathlib import Path
import math
import numpy as np
import pandas as pd
from scipy import stats


ALPHA = 0.05
MU0_X3 = 75.24
LAMBDA_X4 = 0.106
CSV_FILE = "data.csv"


def print_header(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def decision_by_pvalue(p_value: float, alpha: float = ALPHA) -> str:
    if p_value < alpha:
        return "H0 отвергается"
    return "Нет оснований отвергнуть H0"


def check_columns(df: pd.DataFrame):
    required_columns = {"X1", "X2", "X3", "X4"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"В файле отсутствуют столбцы: {missing}")



BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / CSV_FILE

df = pd.read_csv(path, sep=";")
check_columns(df)

x1 = df["X1"].dropna().to_numpy()
x2 = df["X2"].dropna().to_numpy()
x3 = df["X3"].dropna().to_numpy()
x4 = df["X4"].dropna().to_numpy()


# 4.2
print_header("4.2. Проверка H0: EX1 = EX2")

m = len(x1)
n = len(x2)

mean_x1 = np.mean(x1)
mean_x2 = np.mean(x2)

var_x1 = np.var(x1, ddof=1)
var_x2 = np.var(x2, ddof=1)

std_x1 = np.std(x1, ddof=1)
std_x2 = np.std(x2, ddof=1)

sp2 = ((m - 1) * var_x1 + (n - 1) * var_x2) / (m + n - 2)
sp = math.sqrt(sp2)

t_obs = (mean_x1 - mean_x2) / (sp * math.sqrt(1 / m + 1 / n))
df_t = m + n - 2

p_value_t = 2 * stats.t.sf(abs(t_obs), df=df_t)
t_crit = stats.t.ppf(1 - ALPHA / 2, df=df_t)

print(f"n1 = {m}, n2 = {n}")
print(f"Среднее X1 = {mean_x1:.4f}")
print(f"Среднее X2 = {mean_x2:.4f}")
print(f"Исправленная дисперсия X1 = {var_x1:.4f}")
print(f"Исправленная дисперсия X2 = {var_x2:.4f}")
print(f"Стандартное отклонение X1 = {std_x1:.4f}")
print(f"Стандартное отклонение X2 = {std_x2:.4f}")
print(f"Объединённая дисперсия Sp^2 = {sp2:.4f}")
print(f"Sp = {sp:.4f}")
print(f"Степени свободы = {df_t}")
print(f"t_набл = {t_obs:.4f}")
print(f"|t_набл| = {abs(t_obs):.4f}")
print(f"t_кр = {t_crit:.4f}")
print(f"p-value = {p_value_t:.4f}")
print(f"Решение: {decision_by_pvalue(p_value_t)}")


# 4.3
print_header("4.3. Проверка H0: mu = 75.24 для X3")

n3 = len(x3)
mean_x3 = np.mean(x3)
var_x3 = np.var(x3, ddof=1)
std_x3 = np.std(x3, ddof=1)

t_obs_x3 = math.sqrt(n3) * (mean_x3 - MU0_X3) / std_x3
df_x3 = n3 - 1

p_value_x3 = 2 * stats.t.sf(abs(t_obs_x3), df=df_x3)
t_crit_x3 = stats.t.ppf(1 - ALPHA / 2, df=df_x3)

print(f"n = {n3}")
print(f"mu0 = {MU0_X3}")
print(f"Среднее X3 = {mean_x3:.4f}")
print(f"Исправленная дисперсия X3 = {var_x3:.4f}")
print(f"Стандартное отклонение X3 = {std_x3:.4f}")
print(f"Степени свободы = {df_x3}")
print(f"t_набл = {t_obs_x3:.4f}")
print(f"|t_набл| = {abs(t_obs_x3):.4f}")
print(f"t_кр = {t_crit_x3:.4f}")
print(f"p-value = {p_value_x3:.4f}")
print(f"Решение: {decision_by_pvalue(p_value_x3)}")

# 4.4
print_header("4.4. Критерий Манна–Уитни для X1 и X2")

combined = np.concatenate([x1, x2])
ranks = stats.rankdata(combined, method="average")

ranks_x1 = ranks[:m]
ranks_x2 = ranks[m:]

R1 = np.sum(ranks_x1)
R2 = np.sum(ranks_x2)

U1 = R1 - m * (m + 1) / 2
U2 = R2 - n * (n + 1) / 2
U_obs = min(U1, U2)

mann_result = stats.mannwhitneyu(
    x1,
    x2,
    alternative="two-sided",
    method="asymptotic"
)

p_value_mw = mann_result.pvalue

print(f"n1 = {m}, n2 = {n}")
print(f"R1 = {R1:.4f}")
print(f"R2 = {R2:.4f}")
print(f"U1 = {U1:.4f}")
print(f"U2 = {U2:.4f}")
print(f"U_набл = min(U1, U2) = {U_obs:.4f}")
print(f"p-value = {p_value_mw:.4f}")
print(f"Решение: {decision_by_pvalue(p_value_mw)}")


# 4.5
print_header("4.5. Критерий согласия Пирсона для X4")

n4 = len(x4)
r = 8
s = 0

bounds = [0]

for i in range(1, r):
    q = -math.log(1 - i / r) / LAMBDA_X4
    bounds.append(q)

bounds.append(math.inf)

observed = []
interval_labels = []

for left, right in zip(bounds[:-1], bounds[1:]):
    if math.isinf(right):
        count = np.sum(x4 >= left)
        label = f"[{left:.4f}; +inf)"
    else:
        count = np.sum((x4 >= left) & (x4 < right))
        label = f"[{left:.4f}; {right:.4f})"

    observed.append(int(count))
    interval_labels.append(label)

p_i = 1 / r
expected = n4 * p_i

contributions = [((o - expected) ** 2) / expected for o in observed]
chi2_obs = sum(contributions)

df_chi2 = r - s - 1
chi2_crit = stats.chi2.ppf(1 - ALPHA, df=df_chi2)
p_value_chi2 = stats.chi2.sf(chi2_obs, df=df_chi2)

freq_table = pd.DataFrame({
    "№": range(1, r + 1),
    "Интервал": interval_labels,
    "O_i": observed,
    "p_i": [p_i] * r,
    "E_i": [expected] * r,
    "(O_i - E_i)^2 / E_i": contributions
})

print(f"n = {n4}")
print(f"lambda = {LAMBDA_X4}")
print(f"Количество интервалов r = {r}")
print(f"Теоретическая вероятность каждого интервала p_i = {p_i:.4f}")
print(f"Ожидаемая частота каждого интервала E_i = {expected:.4f}")
print()

print("Таблица наблюдаемых и ожидаемых частот:")
print(freq_table.to_string(index=False, formatters={
    "p_i": "{:.4f}".format,
    "E_i": "{:.4f}".format,
    "(O_i - E_i)^2 / E_i": "{:.4f}".format
}))

print()
print(f"Сумма наблюдаемых частот = {sum(observed)}")
print(f"chi2_набл = {chi2_obs:.4f}")
print(f"Степени свободы = r - s - 1 = {r} - {s} - 1 = {df_chi2}")
print(f"chi2_кр = {chi2_crit:.4f}")
print(f"p-value = {p_value_chi2:.4f}")
print(f"Решение: {decision_by_pvalue(p_value_chi2)}")


# Итоговая таблица
print_header("Итоговая таблица")

summary_rows = [
    {
        "Пункт": "4.2",
        "Гипотеза": "H0: EX1 = EX2",
        "Критерий": "Двухвыборочный критерий Стьюдента",
        "Статистика": f"t = {t_obs:.4f}",
        "p-value": f"{p_value_t:.4f}",
        "Решение": decision_by_pvalue(p_value_t),
    },
    {
        "Пункт": "4.3",
        "Гипотеза": "H0: mu = 75.24",
        "Критерий": "Одновыборочный критерий Стьюдента",
        "Статистика": f"t = {t_obs_x3:.4f}",
        "p-value": f"{p_value_x3:.4f}",
        "Решение": decision_by_pvalue(p_value_x3),
    },
    {
        "Пункт": "4.4",
        "Гипотеза": "H0: F_X1(x) = F_X2(x)",
        "Критерий": "Критерий Манна–Уитни",
        "Статистика": f"U = {U_obs:.4f}",
        "p-value": f"{p_value_mw:.4f}",
        "Решение": decision_by_pvalue(p_value_mw),
    },
    {
        "Пункт": "4.5",
        "Гипотеза": "H0: X4 ~ Exp(lambda = 0.106)",
        "Критерий": "Критерий согласия Пирсона",
        "Статистика": f"chi2 = {chi2_obs:.4f}",
        "p-value": f"{p_value_chi2:.4f}",
        "Решение": decision_by_pvalue(p_value_chi2),
    },
]

for row in summary_rows:
    print("-" * 70)
    print(f"Пункт:      {row['Пункт']}")
    print(f"Гипотеза:   {row['Гипотеза']}")
    print(f"Критерий:   {row['Критерий']}")
    print(f"Статистика: {row['Статистика']}")
    print(f"p-value:    {row['p-value']}")
    print(f"Решение:    {row['Решение']}")

print("-" * 70)