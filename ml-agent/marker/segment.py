from dataclasses import dataclass, field
from enum import Enum
from typing import List

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
