import pandas as pd


def calculate_avg_candle_length(df: pd.DataFrame) -> float:
    df["body_length"] = abs(df["close"] - df["open"])
    df["upper_shadow"] = df["high"] - df[["close", "open"]].max(axis=1)
    df["lower_shadow"] = df[["close", "open"]].min(axis=1) - df["low"]
    df["full_length"] = df["upper_shadow"] + df["body_length"] + df["lower_shadow"]
    return df["full_length"].mean()


def mark(df: pd.DataFrame, a_len: int = 5) -> pd.DataFrame:
    df = df.copy().reset_index(drop=True)

    # Приведение к числам
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Вычисление средней длины свечи
    avg = calculate_avg_candle_length(df)
    print(f"Средняя длина свечи (avg) = {avg:.2f}")

    ai_indices = []  # Индексы для Ai
    bi_indices = []  # Индексы для Bi

    # Ищем начало и завершение тренда
    for i in range(2, len(df)):
        h1, h2, h3 = df.loc[i - 2, "high"], df.loc[i - 1, "high"], df.loc[i, "high"]
        l1, l2, l3 = df.loc[i - 2, "low"], df.loc[i - 1, "low"], df.loc[i, "low"]

        # Начало направленного движения (Ai)
        if (h3 > h2 > h1 and l3 > l2 > l1) or (h3 < h2 < h1 and l3 < l2 < l1):  # type: ignore
            ai_indices.append(i)  # Записываем индексы Ai

        # Завершение направленного движения (Bi)
        if (h3 < h2 < h1 and l3 < l2 < l1) or (h3 > h2 > h1 and l3 > l2 > l1):  # type: ignore
            bi_indices.append(i)  # Записываем индексы Bi

    # Отладка: Выводим индексы Ai и Bi
    print(f"Найдено {len(ai_indices)} трендов Ai: {ai_indices}")
    print(f"Найдено {len(bi_indices)} трендов Bi: {bi_indices}")

    # Если нет Ai и Bi, возвращаем пустой DataFrame
    if not ai_indices or not bi_indices:
        return pd.DataFrame()  # Возвращаем пустой DataFrame

    # Создаем новый DataFrame для хранения подходящих сегментов
    final_segments = []

    # Формируем сегменты из Ai и Bi, добавляем только те, где разница в Bi > 0.25 * avg
    for ai, bi in zip(ai_indices, bi_indices):
        # Проверяем, что у нас есть хотя бы несколько свечей до Ai
        if ai >= a_len:
            segment = df.iloc[ai : bi + 1]  # Сегмент от Ai до Bi

            # Отладка: Выводим сегмент
            print(f"Сегмент от Ai = {ai} до Bi = {bi}:")
            print(segment)

            # Проверка для восходящего тренда (если Bi - рост):
            if segment["close"].iloc[0] < segment["close"].iloc[-1]:
                price_diff = (
                    segment["close"].iloc[-1] - segment["open"].iloc[0]
                )  # Изменение цены в сегменте
                print(
                    f"Проверка для восходящего тренда: price_diff = {price_diff}, 0.25 * avg = {0.25 * avg}"
                )
                # Ослабляем порог для добавления в сегмент
                if price_diff > 0.25 * avg:  # Порог до 0.25 * avg
                    print(f"Добавляем восходящий сегмент: {price_diff} > {0.25 * avg}")
                    final_segments.append(segment)

            # Проверка для нисходящего тренда (если Bi - падение):
            elif segment["close"].iloc[0] > segment["close"].iloc[-1]:
                price_diff = (
                    segment["open"].iloc[0] - segment["close"].iloc[-1]
                )  # Изменение цены в сегменте
                print(
                    f"Проверка для нисходящего тренда: price_diff = {price_diff}, 0.25 * avg = {0.25 * avg}"
                )
                # Ослабляем порог для добавления в сегмент
                if price_diff > 0.25 * avg:  # Порог до 0.25 * avg
                    print(f"Добавляем нисходящий сегмент: {price_diff} > {0.25 * avg}")
                    final_segments.append(segment)

    # Если нет подходящих сегментов, возвращаем пустой DataFrame
    if not final_segments:
        print("Нет подходящих сегментов.")
        return pd.DataFrame()

    # Объединяем все сегменты и убираем дубли
    merged_df = (
        pd.concat(final_segments)
        .drop_duplicates(subset="open_time")
        .sort_values("open_time")
        .reset_index(drop=True)
    )
    return merged_df


if __name__ == "__main__":
    # Пути
    input_path = "data/candles/BTCUSDT/test/BTCUSDT-15m-test.csv"
    output_path = "data/candles/BTCUSDT/test/BTCUSDT-15m-ai_bi.csv"

    # Загрузка данных
    df = pd.read_csv(input_path, parse_dates=["open_time"])

    # Приведение к числам
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Применение алгоритма
    result_df = mark(df)

    # Сохранение результата
    result_df.to_csv(output_path, index=False)
    print(f"Сохранено {len(result_df)} свечей в {output_path}")
