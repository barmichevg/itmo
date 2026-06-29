from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
filename = BASE_DIR / 'data.csv'
columns = ['X1', 'X2', 'X3']
out_dir = BASE_DIR / 'rgr_figures'
out_dir.mkdir(exist_ok=True)

if not filename.exists():
    raise FileNotFoundError(f'Файл не найден: {filename}\n')

data = np.genfromtxt(filename, delimiter=',', names=True, encoding='utf-8')
n = len(data)

print(f'Объём выборки: n = {n}')
print()


# вспомогательные функции
def scott_bins(x):
    s = np.std(x, ddof=0)
    h = 3.5 * s * len(x) ** (-1 / 3)
    k = math.ceil((np.max(x) - np.min(x)) / h)
    return max(k, 1), h


def normal_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def get_model_name(col):
    if col == 'X1':
        return 'Exp(λ, c)'
    elif col == 'X2':
        return 'U(a, b)'
    elif col == 'X3':
        return 'N(a, σ)'
    return ''


# 4.1
def analyze_column(name, x):
    x_sorted = np.sort(x)

    x_bar = np.mean(x)
    S2 = np.var(x, ddof=0)
    s2 = np.var(x, ddof=1)
    S = np.std(x, ddof=0)
    s = np.std(x, ddof=1)
    median = np.median(x)
    q1 = np.quantile(x, 0.25)
    q3 = np.quantile(x, 0.75)
    x_min = np.min(x)
    x_max = np.max(x)

    k, h = scott_bins(x)

    print()
    print(name)
    print('Вариационный ряд:')
    print(x_sorted)
    print()

    print('Числовые характеристики:')
    print(f'  x̄   = {x_bar:.4f}')
    print(f'  S²   = {S2:.4f}')
    print(f'  s²   = {s2:.4f}')
    print(f'  S    = {S:.4f}')
    print(f'  s    = {s:.4f}')
    print(f'  me   = {median:.4f}')
    print(f'  Q1   = {q1:.4f}')
    print(f'  Q3   = {q3:.4f}')
    print(f'  min  = {x_min:.2f}')
    print(f'  max  = {x_max:.2f}')
    print(f'  Скотт: k = {k}, h = {h:.4f}')
    print(f'  Гипотеза для 4.2: {get_model_name(name)}')
    print()

    # графики
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # гистограмма
    axes[0].hist(x, bins=k, color='skyblue', edgecolor='black')
    axes[0].axvline(x_bar, color='red', linestyle='--', label=f'x̄ = {x_bar:.2f}')
    axes[0].set_title(f'{name}: гистограмма')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('Частота')
    axes[0].legend()

    # эмпирическая функция распределения
    y = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
    axes[1].step(x_sorted, y, where='post', color='green')
    axes[1].set_title(f'{name}: эмпирическая ФР')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('F_n(x)')
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_dir / f'{name}.png', dpi=150)
    plt.show()


# 4.3
def estimate_params(name, x):
    x_bar = np.mean(x)
    S2 = np.var(x, ddof=0)
    S = np.std(x, ddof=0)
    x_min = np.min(x)
    x_max = np.max(x)

    print()
    print(f'4.3 {name}')

    if name == 'X1':
        lambda_mm = 1 / S
        c_mm = x_bar - S

        c_mle = x_min
        lambda_mle = 1 / (x_bar - c_mle)

        print('Модель: Exp(λ, c)')
        print(f'Метод моментов:               λ = {lambda_mm:.5f}, c = {c_mm:.4f}')
        print(f'Макс. правдоподобие (ММП):    λ = {lambda_mle:.5f}, c = {c_mle:.4f}')

        return {
            'model': 'Exp(λ, c)',
            'lambda_mm': lambda_mm,
            'c_mm': c_mm,
            'lambda_mle': lambda_mle,
            'c_mle': c_mle
        }

    elif name == 'X2':
        a_mm = x_bar - math.sqrt(3 * S2)
        b_mm = x_bar + math.sqrt(3 * S2)

        a_mle = x_min
        b_mle = x_max

        print('Модель: U(a, b)')
        print(f'Метод моментов:               a = {a_mm:.4f}, b = {b_mm:.4f}')
        print(f'Макс. правдоподобие (ММП):    a = {a_mle:.4f}, b = {b_mle:.4f}')

        return {
            'model': 'U(a, b)',
            'a_mm': a_mm,
            'b_mm': b_mm,
            'a_mle': a_mle,
            'b_mle': b_mle
        }

    elif name == 'X3':
        a_mm = x_bar
        sigma_mm = S

        a_mle = x_bar
        sigma_mle = S

        print('Модель: N(a, σ)')
        print(f'Метод моментов:               a = {a_mm:.4f}, σ = {sigma_mm:.4f}')
        print(f'Макс. правдоподобие (ММП):    a = {a_mle:.4f}, σ = {sigma_mle:.4f}')

        return {
            'model': 'N(a, σ)',
            'a_mm': a_mm,
            'sigma_mm': sigma_mm,
            'a_mle': a_mle,
            'sigma_mle': sigma_mle
        }



# 4.4
def estimate_probability(name, x, params):
    x_bar = np.mean(x)
    s = np.std(x, ddof=1)
    x0 = x_bar + s

    m = np.sum(x > x0)
    p_emp = m / len(x)

    print()
    print(f'4.4 {name}')
    print(f'x0 = x̄ + s = {x0:.4f}')
    print(f'Эмпирическая оценка: p_emp = {p_emp:.4f}')

    if name == 'X1':
        c_hat = params['c_mle']
        lambda_hat = params['lambda_mle']
        p_par = math.exp(-lambda_hat * (x0 - c_hat))

    elif name == 'X2':
        a_hat = params['a_mle']
        b_hat = params['b_mle']
        p_par = (b_hat - x0) / (b_hat - a_hat)

    elif name == 'X3':
        a_hat = params['a_mle']
        sigma_hat = params['sigma_mle']
        z = (x0 - a_hat) / sigma_hat
        p_par = 1 - normal_cdf(z)

    print(f'Параметрическая оценка: p_par = {p_par:.4f}')
    print(f'Разность: |p_emp - p_par| = {abs(p_emp - p_par):.4f}')

    return {
        'x0': x0,
        'p_emp': p_emp,
        'p_par': p_par
    }


# 4.5 
def grouped_moments(name, x):
    n = len(x)
    S = np.std(x, ddof=0)
    h = 3.5 * S * n ** (-1 / 3)
    k = math.ceil((np.max(x) - np.min(x)) / h)

    counts, edges = np.histogram(x, bins=k)
    mids = (edges[:-1] + edges[1:]) / 2

    x_g = np.sum(counts * mids) / n
    s2_g = np.sum(counts * (mids - x_g) ** 2) / (n - 1)

    x_bar = np.mean(x)
    s2 = np.var(x, ddof=1)

    print()
    print(f'4.5 {name}')
    print(f'Сгруппированное среднее:    x_g  = {x_g:.4f}')
    print(f'Сгруппированная дисперсия:  s²_g = {s2_g:.4f}')
    print(f'По исходным данным:         x̄    = {x_bar:.4f}')
    print(f'По исходным данным:         s²    = {s2:.4f}')
    print(f'Разность по среднему:       {abs(x_g - x_bar):.4f}')
    print(f'Разность по дисперсии:      {abs(s2_g - s2):.4f}')

    return {
        'x_g': x_g,
        's2_g': s2_g
    }


# 4.6
def confidence_intervals(name, x):
    alpha = 0.05
    z_crit = 1.96

    n = len(x)
    x_bar = np.mean(x)
    s = np.std(x, ddof=1)
    s2 = np.var(x, ddof=1)

    mean_left = x_bar - z_crit * s / math.sqrt(n)
    mean_right = x_bar + z_crit * s / math.sqrt(n)

    print()
    print(f'4.6 {name}')
    print(f'Асимптотический ДИ для E(X): ({mean_left:.4f}; {mean_right:.4f})')

    result = {
        'mean_left': mean_left,
        'mean_right': mean_right
    }

    if name == 'X3':
        t_crit = 1.972
        chi2_left = 161.8262
        chi2_right = 239.9597

        mu_left = x_bar - t_crit * s / math.sqrt(n)
        mu_right = x_bar + t_crit * s / math.sqrt(n)

        sigma2_left = (n - 1) * s2 / chi2_right
        sigma2_right = (n - 1) * s2 / chi2_left

        print(f'Точный ДИ для μ:            ({mu_left:.4f}; {mu_right:.4f})')
        print(f'Точный ДИ для σ²:           ({sigma2_left:.4f}; {sigma2_right:.4f})')

        result['mu_left'] = mu_left
        result['mu_right'] = mu_right
        result['sigma2_left'] = sigma2_left
        result['sigma2_right'] = sigma2_right

    return result



all_params = {}
all_prob = {}
all_grouped = {}
all_ci = {}


for col in columns:
    analyze_column(col, data[col])

for col in columns:
    all_params[col] = estimate_params(col, data[col])

for col in columns:
    all_prob[col] = estimate_probability(col, data[col], all_params[col])

for col in columns:
    all_grouped[col] = grouped_moments(col, data[col])

for col in columns:
    all_ci[col] = confidence_intervals(col, data[col])

final_summary(all_params, all_ci)