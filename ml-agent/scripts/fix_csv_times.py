import os

import pandas as pd

DATA_DIR = os.path.join("data", "candles")


def fix_timestamps_in_csv_files():
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".csv"):
            continue

        filepath = os.path.join(DATA_DIR, filename)
        print(f"🛠 Fixing timestamps in: {filepath}")

        df = pd.read_csv(filepath)

        try:
            df["open_time"] = pd.to_datetime(df["open_time"].astype("int64"), unit="ms")
            df["close_time"] = pd.to_datetime(
                df["close_time"].astype("int64"), unit="ms"
            )
        except Exception as e:
            print(f"⚠️ Failed to process {filename}: {e}")
            continue

        df.to_csv(filepath, index=False)
        print(f"✅ Saved updated file: {filepath}")


if __name__ == "__main__":
    fix_timestamps_in_csv_files()
