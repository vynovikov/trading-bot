import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.config import get_days, get_interval, get_symbols
from services.data_loader import get_or_fetch_candles

print("🎯 get_symbols() →", get_symbols())


SYMBOLS = get_symbols()
INTERVAL = get_interval()
DAYS = get_days()

TO_TS = int(time.time() * 1000)
FROM_TS = TO_TS - DAYS * 24 * 60 * 60 * 1000

for symbol in SYMBOLS:
    df = get_or_fetch_candles(symbol, INTERVAL, FROM_TS, TO_TS)
    print(f"🔹 {symbol}: {len(df)} candles loaded.")
