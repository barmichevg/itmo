from pathlib import Path
import zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor


ZIP_NAME = "online+news+popularity.zip"
CSV_NAME = "OnlineNewsPopularity.csv"
TARGET_COLUMN = "shares"
DROP_COLUMNS = ["url", "timedelta"]
N_FEATURES = 15
RESULTS_DIR_NAME = "results"
GB_N_ESTIMATORS = 30
NC_MAX = 3
N_STEPS = 4
INIT_PHEROMONE = 0.2
RO = 0.2
EXPLOITATION_PROB = 0.7
ALPHA = 1.0
N_ANTS = 5
UFSACO_RANDOM_STATE = 28
EPS = 1e-12


# Работа с файлами
def get_script_dir():
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()


def find_csv_file(script_dir):
    csv_path = script_dir / CSV_NAME

    if csv_path.exists():
        return csv_path

    zip_path = script_dir / ZIP_NAME
    extract_dir = script_dir / "data"

    if zip_path.exists():
        if not extract_dir.exists():
            print("Распаковка архива...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

        csv_files = list(extract_dir.rglob(CSV_NAME))
        if csv_files:
            return csv_files[0]

    raise FileNotFoundError(
        f"Не найден файл {CSV_NAME} или архив {ZIP_NAME} в папке:\n{script_dir}"
    )


def create_results_dir(script_dir):
    results_dir = script_dir / RESULTS_DIR_NAME
    results_dir.mkdir(exist_ok=True)
    return results_dir


# Загрузка и подготовка данных
def load_dataset(script_dir):
    csv_path = find_csv_file(script_dir)
    print(f"Загрузка файла:\n{csv_path}")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    return df


def prepare_data(df):
    df = df.copy()

    for column in DROP_COLUMNS:
        if column in df.columns:
            df = df.drop(columns=[column])

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Целевой признак {TARGET_COLUMN} не найден.")

    df = df.dropna()

    y = df[TARGET_COLUMN]
    X = df.drop(columns=[TARGET_COLUMN])
    X = X.select_dtypes(include=["number"])

    scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

    return X, X_scaled, y


# Gradient Boosting
def gradient_boosting_selection(X, y, results_dir):
    print("\nGradient Boosting")
    print("=" * 70)

    model = GradientBoostingRegressor(
        n_estimators=GB_N_ESTIMATORS,
        max_depth=4,
        min_samples_split=10,
        learning_rate=0.01,
        random_state=42
    )

    print("Обучение модели...")
    model.fit(X, y)
    print("Обучение завершено.")

    # таблица важностей
    importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    top_df = importance_df.head(N_FEATURES)
    gb_features = top_df["feature"].tolist()

    print(f"\nТоп-{N_FEATURES} признаков по Gradient Boosting:")
    print(top_df)

    importance_df.to_csv(
        results_dir / "gradient_boosting_all_features.csv",
        index=False,
        encoding="utf-8-sig"
    )

    top_df.to_csv(
        results_dir / "gradient_boosting_top_features.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return gb_features


# UFSACO
# схожесть между вершинами
def cosine_similarity_matrix(X_scaled):
    data = X_scaled.to_numpy()

    norms = np.linalg.norm(data, axis=0)
    norms[norms == 0] = EPS

    similarity = (data.T @ data) / (norms[:, None] * norms[None, :])
    similarity = np.abs(similarity)
    similarity = np.clip(similarity, EPS, None)

    np.fill_diagonal(similarity, 1.0)

    return similarity


# основной алгритм UFSACO
def ufsaco_selection(X_scaled, results_dir):
    print("\nUFSACO")
    print("=" * 70)

    rng = np.random.default_rng(UFSACO_RANDOM_STATE)

    feature_names = X_scaled.columns.tolist()
    n_features_start = len(feature_names)

    similarity = cosine_similarity_matrix(X_scaled)

    tau = INIT_PHEROMONE * np.ones(n_features_start)

    # цикл муравьиной колонии
    for count in range(NC_MAX):
        ants_pos = rng.choice(
            n_features_start,
            size=N_ANTS,
            p=tau / tau.sum()
        )

        visits = np.zeros(n_features_start)

        # для каждого муравья сохраняем множество посещенных вершин
        nodes_visited = {
            (k, i): set()
            for k in range(N_ANTS)
            for i in range(n_features_start)
        }

        # шаги муравьев
        for step in range(N_STEPS):
            for k in range(N_ANTS):
                i = int(ants_pos[k])

                visited = nodes_visited[(k, i)]
                unvisited = list((set(range(n_features_start)) - visited) - {i})

                # расчет вероятностей выбора
                node_score = np.array([
                    tau[j] / np.power(similarity[i, j], ALPHA)
                    for j in unvisited
                ])

                # выбор следующей вершины p
                q = rng.uniform()

                if q <= EXPLOITATION_PROB:
                    jj = int(np.argmax(node_score))
                else:
                    probabilities = node_score / node_score.sum()
                    jj = int(rng.choice(len(unvisited), p=probabilities))
                    
                # считаем посещение вершин
                j = unvisited[jj]
                ants_pos[k] = j
                nodes_visited[(k, i)].add(j)
                visits[j] += 1

        # обновляем феромон
        total_visits = visits.sum()
        tau = (1 - RO) * tau + (visits / total_visits)

    # итоговые признаки
    selected_indexes = tau.argsort()[::-1][:N_FEATURES]
    aco_features = [feature_names[i] for i in selected_indexes]

    aco_df = pd.DataFrame({
        "order": range(1, len(aco_features) + 1),
        "feature": aco_features,
        "pheromone": tau[selected_indexes]
    })

    print(f"\nПризнаки, выбранные UFSACO:")
    print(aco_df)

    aco_df.to_csv(results_dir / "ufsaco_features.csv", index=False, encoding="utf-8-sig")

    return aco_features


# Сравнение признаков
def compare_features(gb_features, aco_features, results_dir):
    intersection = sorted(set(gb_features) & set(aco_features))

    comparison_df = pd.DataFrame({
        "Gradient_Boosting": pd.Series(gb_features),
        "UFSACO": pd.Series(aco_features),
        "Intersection": pd.Series(intersection)
    })

    print("\nСравнение множеств признаков")
    print("=" * 70)
    print(comparison_df)

    print(f"\nРазмер пересечения: {len(intersection)}")

    if len(intersection) >= 4:
        print("Условие задания выполнено: пересечение содержит не менее 4 признаков.")
    else:
        print("Условие задания НЕ выполнено.")
        print("Попробуйте увеличить N_FEATURES до 20 или изменить UFSACO_RANDOM_STATE.")

    comparison_df.to_csv(results_dir / "feature_sets_comparison.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame({"feature": intersection}).to_csv(
        results_dir / "intersection_features.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return intersection


def main():
    script_dir = get_script_dir()
    results_dir = create_results_dir(script_dir)

    df = load_dataset(script_dir)

    print("\nИсходный датасет:")
    print(f"Размер: {df.shape}")
    print(f"Количество пропусков: {df.isnull().sum().sum()}")

    X, X_scaled, y = prepare_data(df)

    print("\nПосле подготовки:")
    print(f"X: {X.shape}")
    print(f"X_scaled: {X_scaled.shape}")
    print(f"y: {y.shape}")

    gb_features = gradient_boosting_selection(X, y, results_dir)
    aco_features = ufsaco_selection(X_scaled, results_dir)

    compare_features(gb_features, aco_features, results_dir)

    print(f"\nВсе файлы сохранены в папку:\n{results_dir}")


if __name__ == "__main__":
    main()