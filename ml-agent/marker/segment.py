from dataclasses import dataclass, field
from enum import Enum
from typing import List

import pandas as pd

from marker.candle import Candle


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    UNKNOWN = "unknown"


@dataclass
class TradeParams:
    direction: Direction = Direction.UNKNOWN
    finish: bool = False
    tp: float = 0.0
    sl: float = 0.0


@dataclass
class Segment:
    Pre: List[Candle] = field(default_factory=list)
    Trend: List[Candle] = field(default_factory=list)
    Params: TradeParams = field(default_factory=lambda: TradeParams())

    def get_direction(self) -> Direction:
        return self.Params.direction

    def set_direction(self, direction: Direction):
        self.Params.direction = direction

    def set_finish(self):
        self.Params.finish = True

    def get_finish(self) -> bool:
        return self.Params.finish

    def add_to_pre(self, df: pd.DataFrame, idx: int, a_len: int):
        for i in range(idx - a_len, idx):
            self.Pre.append(self.idx_to_candle(i, df))

    def add_to_trend(self, *candles: Candle):
        self.Trend.extend(candles)

    def idx_to_candle(self, idx: int, df: pd.DataFrame) -> Candle:
        return Candle(
            high=df.iloc[idx]["high"],
            low=df.iloc[idx]["low"],
            open=df.iloc[idx]["open"],
            close=df.iloc[idx]["close"],
            volume=df.iloc[idx]["volume"],
        )
