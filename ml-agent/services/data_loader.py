import os

import grpc
import pandas as pd

from client.grpc_client import StockInteractorClient
from services.config import get_backend_host, get_backend_port

DATA_DIR = os.path.join("data", "candles")
os.makedirs(DATA_DIR, exist_ok=True)


def get_or_fetch_candles(
    symbol: str, interval: str, from_ts: int, to_ts: int
) -> pd.DataFrame:
    filename = f"{symbol}-{interval}-{from_ts}-{to_ts}.csv"
    filepath = os.path.join(DATA_DIR, filename)

    if os.path.exists(filepath):
        print(f"📁 Found cached file: {filepath}")
        return pd.read_csv(filepath)

    print(f"🔌 Fetching from gRPC: {symbol} {interval}")
    client = StockInteractorClient(host=get_backend_host(), port=get_backend_port())
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
    except grpc.RpcError as e:
        raise RuntimeError(f"gRPC error for {symbol}: {e.code()} - {e.details()}")

    df = pd.DataFrame(all_candles)
    df.to_csv(filepath, index=False)
    print(f"✅ Saved to {filepath}")
    return df
