import pandas as pd

# Папки
input_folder_name = "data/candles/BTCUSDT/full/"
output_folder_name = "data/candles/BTCUSDT/test/"

# Файлы
input_file_name = "BTCUSDT-15m-1717662543351-1749198543351.csv"
output_file_name = "BTCUSDT-15m-test.csv"

# Пути к файлам
input_file = f"{input_folder_name}{input_file_name}"
output_file = f"{output_folder_name}{output_file_name}"

# Загрузка CSV
df = pd.read_csv(input_file, parse_dates=["open_time"])
df = df.sort_values("open_time").reset_index(drop=True)

# Вычисляем разницу между соседними свечами
df["time_diff"] = df["open_time"].diff()

# Флаг, где интервал ровно 15 минут
is_continuous = df["time_diff"] == pd.Timedelta(minutes=15)

# Ищем индексы, где цепочка прерывается
df["chain_id"] = (~is_continuous).cumsum()

# Выбираем самую длинную цепочку
longest_chain_id = df["chain_id"].value_counts().idxmax()
chain_df = df[df["chain_id"] == longest_chain_id].copy()

# Берем первые 200 свечей из неё
df_200 = chain_df.head(200).drop(columns=["time_diff", "chain_id"])

# Сохраняем в файл
df_200.to_csv(output_file, index=False)

print(
    f"Сохранено {len(df_200)} свечей из самой длинной цепочки без разрывов по 15 минут в {output_file}"
)
