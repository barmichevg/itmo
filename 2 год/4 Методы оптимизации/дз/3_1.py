from pathlib import Path
import zipfile
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


ZIP_NAME = "online+news+popularity.zip"
CSV_NAME = "OnlineNewsPopularity.csv"
TARGET_COLUMN = "shares"
DROP_COLUMNS = ["url", "timedelta"]


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

    if not zip_path.exists():
        raise FileNotFoundError(
            f"Не найден файл {CSV_NAME} или архив {ZIP_NAME} в папке:\n{script_dir}"
        )

    if not extract_dir.exists():
        print("Распаковка архива...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        print("Архив распакован.")

    csv_files = list(extract_dir.rglob(CSV_NAME))

    if not csv_files:
        raise FileNotFoundError(f"Файл {CSV_NAME} не найден после распаковки.")

    return csv_files[0]


def load_dataset():
    script_dir = get_script_dir()
    csv_path = find_csv_file(script_dir)
    print(f"Загрузка файла:\n{csv_path}")
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    return df


# Подготовка данных
def prepare_data(df):
    df = df.copy()

    # Удаляем непредиктивные признаки
    for column in DROP_COLUMNS:
        if column in df.columns:
            df = df.drop(columns=[column])

    # Удаляем строки с пропусками
    df = df.dropna()

    # Отделяем целевой признак
    y = df[TARGET_COLUMN]
    X = df.drop(columns=[TARGET_COLUMN])

    # Оставляем только числовые признаки
    X = X.select_dtypes(include=["number"])

    # Нормируем признаки для UFSACO
    scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)

    return X, X_scaled, y


# Основной запуск
def main():
    df = load_dataset()

    print("\nИсходный датасет:")
    print(f"Размер: {df.shape}")
    print(f"Количество пропусков: {df.isnull().sum().sum()}")

    X, X_scaled, y = prepare_data(df)

    print("\nПосле подготовки:")
    print(f"Размер X: {X.shape}")
    print(f"Размер X_scaled: {X_scaled.shape}")
    print(f"Размер y: {y.shape}")

    print("\nЦелевой признак:")
    print(TARGET_COLUMN)

    print("\nПервые 5 значений y:")
    print(y.head())


if __name__ == "__main__":
    main()