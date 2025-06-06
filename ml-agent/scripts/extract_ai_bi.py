import pandas as pd


def extract_ai_bi_segments(df: pd.DataFrame, a_len: int = 5) -> pd.DataFrame:
    df = df.copy().reset_index(drop=True)
    bi_indices = []

    for i in range(2, len(df)):
        h1, h2, h3 = df.loc[i - 2, "high"], df.loc[i - 1, "high"], df.loc[i, "high"]
        l1, l2, l3 = df.loc[i - 2, "low"], df.loc[i - 1, "low"], df.loc[i, "low"]

        # Начало роста
        if h3 > h2 > h1 and l3 > l2 > l1:  # type: ignore
            bi_indices.append(i - 2)

        # Начало падения
        elif h3 < h2 < h1 and l3 < l2 < l1:  # type: ignore
            bi_indices.append(i - 2)

        # Завершение роста
        elif h3 < h2 < h1 and l3 < l2 < l1:  # type: ignore
            bi_indices.append(i - 2)

        # Завершение падения
        elif h3 > h2 > h1 and l3 > l2 > l1:  # type: ignore
            bi_indices.append(i - 2)

    segments = []
    for bi in sorted(set(bi_indices)):
        if bi >= a_len:
            segment = df.iloc[bi - a_len : bi + 1]
            segments.append(segment)

    merged_df = (
        pd.concat(segments)
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
    result_df = extract_ai_bi_segments(df)

    # Сохранение результата
    result_df.to_csv(output_path, index=False)
    print(f"Сохранено {len(result_df)} свечей в {output_path}")
