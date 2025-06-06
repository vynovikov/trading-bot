import mplfinance as mpf
import pandas as pd

# Пути к файлам CSV
folder_name = "data/candles/BTCUSDT/test/"
file_name = "BTCUSDT-15m-ai_bi.csv"
png_file_name = "BTCUSDT-15m-ai_bi-candles.png"

# Загрузка CSV
df = pd.read_csv(f"{folder_name}{file_name}", parse_dates=["open_time"])

# Приведение к нужному формату:
df.set_index("open_time", inplace=True)
df = df[["open", "high", "low", "close", "volume"]]  # Только нужные колонки

# Путь к сохранению
output_path = f"{folder_name}{png_file_name}"

# Отрисовка свечей и сохранение
mpf.plot(
    df,
    type="candle",
    style="charles",
    volume=True,
    mav=(9, 21),  # Можно убрать или настроить
    title="Candlestick Chart",
    ylabel="Price",
    ylabel_lower="Volume",
    savefig=output_path,
)

print(f"Свечной график сохранен в {output_path}")
