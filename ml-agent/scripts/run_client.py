import os
import sys

import grpc
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from client.grpc_client import StockInteractorClient

symbol = "BTCUSDT"
interval = "1m"
from_ts = 1717200000000
to_ts = 1717203600000

filename = f"{symbol}-{interval}-{from_ts}-{to_ts}.csv"
filepath = os.path.join("data", "candles", filename)

if os.path.exists(filepath):
    print(f"📁 Found cached file: {filepath}")
    df = pd.read_csv(filepath)
else:
    print("🔌 Fetching from stock-interactor...")
    client = StockInteractorClient(port=5002)
    all_candles = []

    try:
        for response in client.get_history(symbol, interval, from_ts, to_ts):
            for candle in response.candles:
                all_candles.append(
                    {
                        "open_time": candle.open_time,
                        "open": candle.open,
                        "high": candle.high,
                        "low": candle.low,
                        "close": candle.close,
                        "volume": candle.volume,
                    }
                )
        df = pd.DataFrame(all_candles)
        df.to_csv(filepath, index=False)
        print(f"✅ Saved to {filepath}")
    except grpc.RpcError as e:
        print(f"❌ gRPC Error: {e.code()} - {e.details()}")
        sys.exit(1)

print(df.head())
