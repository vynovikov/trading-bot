import pandas as pd

# Загрузка CSV-файла для анализа
file_path = "data/candles/BTCUSDT/test/BTCUSDT-15m-test.csv"
df = pd.read_csv(file_path, parse_dates=["open_time"])

# Подсчёт средней длины свечей с учётом теней
df["body_length"] = abs(df["close"] - df["open"])
df["upper_shadow"] = df["high"] - df[["close", "open"]].max(axis=1)
df["lower_shadow"] = df[["close", "open"]].min(axis=1) - df["low"]
df["full_length"] = df["upper_shadow"] + df["body_length"] + df["lower_shadow"]

avg_candle_length = df["full_length"].mean()

# Спред инструмента (в среднем)
spread = (
    (df["ask"] - df["bid"]).mean()
    if "ask" in df.columns and "bid" in df.columns
    else None
)

print(avg_candle_length)
