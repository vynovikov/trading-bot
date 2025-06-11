from typing import NamedTuple


class Candle(NamedTuple):
    high: float
    low: float
    open: float
    close: float
    volume: float
