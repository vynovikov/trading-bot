from typing import List

import pandas as pd

from marker.candle import Candle
from marker.segment import Direction, Segment, TradeParams


class Marker:
    def __init__(self, a_len: int = 4):
        self.a_len = a_len  # Number of candles before trend

    def mark(self, df: pd.DataFrame) -> List[Segment]:
        if len(df) < self.a_len + 6:  # Not enough data to form a segment
            return []

        avg = self.calculate_avg_candle_length(df)
        segments: List[Segment] = []
        segment = Segment()
        i = self.a_len

        while i < len(df) - 2:
            c1 = self.idx_to_candle(i, df)
            c2 = self.idx_to_candle(i + 1, df)
            c3 = self.idx_to_candle(i + 2, df)

            if c1.low <= c2.low <= c3.low and c1.high <= c2.high <= c3.high:
                match segment.Params.direction:
                    case Direction.UNKNOWN:
                        self.add_a_to_segment(df, segment, i)
                        segment.Params.direction = Direction.UP

                        segment.Trend.append(c1)
                        segment.Trend.append(c2)
                        segment.Trend.append(c3)

                        i += 3
                        continue
                    case Direction.UP:
                        segment.Trend.append(c1)
                        segment.Trend.append(c2)
                        segment.Trend.append(c3)

                        i += 3
                        continue
                    case Direction.DOWN:
                        segment.Trend.append(c1)
                        segment.Params.finish = True

                        i += 1
                        continue
            if c1.low > c2.low > c3.low and c1.high > c2.high > c3.high:
                match segment.Params.direction:
                    case Direction.UNKNOWN:
                        self.add_a_to_segment(df, segment, i)
                        segment.Params.direction = Direction.DOWN
                        segment.Trend.append(c1)
                        continue
                    case Direction.UP:
                        segment.Trend.append(c1)
                        segment.Params.finish = True

            if (
                c1.high <= c2.high
                and c1.high > c3.high
                and segment.Params.direction == Direction.UP
            ):
                segment.Params.finish = True
                segment.Trend.append(c1)
                segment.Trend.append(c2)

                i += 2

            # if (
            #    c1.low >= c2.low
            #    and c1.low >= c3.low
            #    and c1.high >= c2.high
            #    and c1.high >= c3.high
            #    and segment.Params.direction == Direction.DOWN
            # ):
            #    segment.Params.finish = True
            #    segment.Trend.append(c1)

            if segment.Params.finish and self.delta(segment) > 2.5 * avg:
                segments.append(segment)

            i += 1

        return segments

    def calculate_avg_candle_length(self, df: pd.DataFrame) -> float:
        df["body_length"] = abs(df["close"] - df["open"])
        df["upper_shadow"] = df["high"] - df[["close", "open"]].max(axis=1)
        df["lower_shadow"] = df[["close", "open"]].min(axis=1) - df["low"]
        df["full_length"] = df["upper_shadow"] + df["body_length"] + df["lower_shadow"]

        return df["full_length"].mean()

    def idx_to_candle(self, idx: int, df: pd.DataFrame) -> Candle:
        return Candle(
            high=df.iloc[idx]["high"],
            low=df.iloc[idx]["low"],
            open=df.iloc[idx]["open"],
            close=df.iloc[idx]["close"],
            volume=df.iloc[idx]["volume"],
        )

    def add_a_to_segment(self, df: pd.DataFrame, segment: Segment, idx: int):
        if idx < self.a_len:
            return

        for i in range(idx - self.a_len, idx):
            segment.Pre.append(self.idx_to_candle(i, df))

    def delta(self, segment: Segment) -> float:
        if not segment.Trend:
            return 0.0

        first_candle = segment.Trend[0]
        last_candle = segment.Trend[-1]

        match segment.Params.direction:
            case Direction.UP:
                return last_candle.high - first_candle.open
            case Direction.DOWN:
                return first_candle.open - last_candle.low
            case _:
                return 0.0
