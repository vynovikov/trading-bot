import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
import pytest

from marker.candle import Candle
from marker.marker import Marker
from marker.segment import Direction, Segment, TradeParams

test_cases = [
    {
        "name": "0. Not enough data",
        "df": pd.DataFrame(
            [
                {"high": 1.0, "low": 0.9, "open": 0.95, "close": 0.96, "volume": 1000},
                {"high": 1.0, "low": 0.9, "open": 0.95, "close": 0.95, "volume": 1000},
            ]
        ),
        "expected": [],
    },
    {
        "name": "1. No trend",
        "df": pd.DataFrame(
            [
                {
                    "high": 1.01,
                    "low": 0.99,
                    "open": 1.00,
                    "close": 1.00,
                    "volume": 1000,
                },
                {
                    "high": 1.02,
                    "low": 1.00,
                    "open": 1.01,
                    "close": 1.01,
                    "volume": 1000,
                },
                {
                    "high": 1.03,
                    "low": 1.01,
                    "open": 1.02,
                    "close": 1.02,
                    "volume": 1000,
                },
                {
                    "high": 1.04,
                    "low": 1.02,
                    "open": 1.03,
                    "close": 1.03,
                    "volume": 1000,
                },
                {
                    "high": 1.05,
                    "low": 1.03,
                    "open": 1.04,
                    "close": 1.04,
                    "volume": 1000,
                },
                {
                    "high": 1.06,
                    "low": 1.04,
                    "open": 1.05,
                    "close": 1.05,
                    "volume": 1000,
                },
                {
                    "high": 1.07,
                    "low": 1.05,
                    "open": 1.06,
                    "close": 1.06,
                    "volume": 1000,
                },
                {
                    "high": 1.08,
                    "low": 1.06,
                    "open": 1.07,
                    "close": 1.07,
                    "volume": 1000,
                },
                {
                    "high": 1.09,
                    "low": 1.07,
                    "open": 1.08,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.10,
                    "low": 1.08,
                    "open": 1.09,
                    "close": 1.09,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [],
    },
    {
        "name": "2. Uptrend with second candle stopping trend",
        "df": pd.DataFrame(
            [
                # Flat candles before uptrend
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                {
                    "high": 1.01,
                    "low": 0.99,
                    "open": 1.00,
                    "close": 1.00,
                    "volume": 1000,
                },
                {
                    "high": 1.02,
                    "low": 1.00,
                    "open": 1.01,
                    "close": 1.01,
                    "volume": 1000,
                },
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                # Start of uptrend (strictly increasing highs and lows)
                {
                    "high": 1.05,
                    "low": 1.02,
                    "open": 1.03,
                    "close": 1.04,
                    "volume": 1000,
                },
                {
                    "high": 1.08,
                    "low": 1.05,
                    "open": 1.06,
                    "close": 1.07,
                    "volume": 1000,
                },
                {
                    "high": 1.11,
                    "low": 1.08,
                    "open": 1.09,
                    "close": 1.10,
                    "volume": 1000,
                },
                # End of uptrend (lows and highs no longer increasing)
                {
                    "high": 1.12,
                    "low": 1.08,
                    "open": 1.10,
                    "close": 1.11,
                    "volume": 1000,
                },
                {
                    "high": 1.11,
                    "low": 1.07,
                    "open": 1.11,
                    "close": 1.09,
                    "volume": 1000,
                },
                {
                    "high": 1.12,
                    "low": 1.08,
                    "open": 1.11,
                    "close": 1.11,
                    "volume": 1000,
                },
                # Flat after trend
                {
                    "high": 1.12,
                    "low": 1.07,
                    "open": 1.09,
                    "close": 1.08,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(
                        high=np.float64(1.00),
                        low=np.float64(0.98),
                        open=0.99,
                        close=0.99,
                        volume=1000,
                    ),
                    Candle(
                        high=np.float64(1.01),
                        low=np.float64(0.99),
                        open=1.00,
                        close=1.00,
                        volume=1000,
                    ),
                    Candle(
                        high=np.float64(1.02),
                        low=1.00,
                        open=1.01,
                        close=1.01,
                        volume=1000,
                    ),
                    Candle(
                        high=np.float64(1.00),
                        low=0.98,
                        open=0.99,
                        close=0.99,
                        volume=1000,
                    ),
                ],
                Trend=[
                    Candle(
                        high=np.float64(1.05),
                        low=np.float64(1.02),
                        open=np.float64(1.03),
                        close=np.float64(1.04),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.08),
                        low=np.float64(1.05),
                        open=np.float64(1.06),
                        close=np.float64(1.07),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.11),
                        low=np.float64(1.08),
                        open=np.float64(1.09),
                        close=np.float64(1.10),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.12),
                        low=np.float64(1.08),
                        open=np.float64(1.10),
                        close=np.float64(1.11),
                        volume=np.float64(1000),
                    ),
                ],
                Params=TradeParams(
                    direction=Direction.UP,
                    finish=True,
                    tp=0.0,
                    sl=0.0,
                ),
            )
        ],
    },
    {
        "name": "3. Uptrend with third candle stopping trend",
        "df": pd.DataFrame(
            [
                # Flat candles before uptrend
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                {
                    "high": 1.01,
                    "low": 0.99,
                    "open": 1.00,
                    "close": 1.00,
                    "volume": 1000,
                },
                {
                    "high": 1.02,
                    "low": 1.00,
                    "open": 1.01,
                    "close": 1.01,
                    "volume": 1000,
                },
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                # Start of uptrend (strictly increasing highs and lows)
                {
                    "high": 1.05,
                    "low": 1.02,
                    "open": 1.03,
                    "close": 1.04,
                    "volume": 1000,
                },
                {
                    "high": 1.08,
                    "low": 1.05,
                    "open": 1.06,
                    "close": 1.07,
                    "volume": 1000,
                },
                {
                    "high": 1.11,
                    "low": 1.08,
                    "open": 1.09,
                    "close": 1.10,
                    "volume": 1000,
                },
                # End of uptrend (lows and highs no longer increasing)
                {
                    "high": 1.12,
                    "low": 1.08,
                    "open": 1.10,
                    "close": 1.11,
                    "volume": 1000,
                },
                {
                    "high": 1.12,
                    "low": 1.08,
                    "open": 1.11,
                    "close": 1.11,
                    "volume": 1000,
                },
                {
                    "high": 1.11,
                    "low": 1.07,
                    "open": 1.11,
                    "close": 1.09,
                    "volume": 1000,
                },
                # Flat after trend
                {
                    "high": 1.12,
                    "low": 1.07,
                    "open": 1.09,
                    "close": 1.08,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(
                        high=np.float64(1.00),
                        low=np.float64(0.98),
                        open=0.99,
                        close=0.99,
                        volume=1000,
                    ),
                    Candle(
                        high=np.float64(1.01),
                        low=np.float64(0.99),
                        open=1.00,
                        close=1.00,
                        volume=1000,
                    ),
                    Candle(
                        high=np.float64(1.02),
                        low=1.00,
                        open=1.01,
                        close=1.01,
                        volume=1000,
                    ),
                    Candle(
                        high=np.float64(1.00),
                        low=0.98,
                        open=0.99,
                        close=0.99,
                        volume=1000,
                    ),
                ],
                Trend=[
                    Candle(
                        high=np.float64(1.05),
                        low=np.float64(1.02),
                        open=np.float64(1.03),
                        close=np.float64(1.04),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.08),
                        low=np.float64(1.05),
                        open=np.float64(1.06),
                        close=np.float64(1.07),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.11),
                        low=np.float64(1.08),
                        open=np.float64(1.09),
                        close=np.float64(1.10),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.12),
                        low=np.float64(1.08),
                        open=np.float64(1.10),
                        close=np.float64(1.11),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.12),
                        low=np.float64(1.08),
                        open=np.float64(1.11),
                        close=np.float64(1.11),
                        volume=np.float64(1000),
                    ),
                ],
                Params=TradeParams(
                    direction=Direction.UP,
                    finish=True,
                    tp=0.0,
                    sl=0.0,
                ),
            )
        ],
    },
    {
        "name": "4. Downtrend with second candle stopping trend",
        "df": pd.DataFrame(
            [
                # Flat candles before downtrend
                {
                    "high": 1.15,
                    "low": 1.13,
                    "open": 1.14,
                    "close": 1.14,
                    "volume": 1000,
                },
                {
                    "high": 1.14,
                    "low": 1.12,
                    "open": 1.13,
                    "close": 1.13,
                    "volume": 1000,
                },
                {
                    "high": 1.13,
                    "low": 1.11,
                    "open": 1.12,
                    "close": 1.12,
                    "volume": 1000,
                },
                {
                    "high": 1.15,
                    "low": 1.13,
                    "open": 1.14,
                    "close": 1.14,
                    "volume": 1000,
                },
                # Start of downtrend (strictly decreasing highs and lows)
                {
                    "high": 1.14,
                    "low": 1.08,
                    "open": 1.14,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.10,
                    "low": 1.04,
                    "open": 1.08,
                    "close": 1.05,
                    "volume": 1000,
                },
                {
                    "high": 1.06,
                    "low": 1.02,
                    "open": 1.05,
                    "close": 1.02,
                    "volume": 1000,
                },
                # End of downtrend (highs and lows no longer decreasing)
                {
                    "high": 1.03,
                    "low": 1.01,
                    "open": 1.02,
                    "close": 1.02,
                    "volume": 1000,
                },
                {
                    "high": 1.04,
                    "low": 1.02,
                    "open": 1.02,
                    "close": 1.03,
                    "volume": 1000,
                },
                {
                    "high": 1.03,
                    "low": 1.01,
                    "open": 1.02,
                    "close": 1.02,
                    "volume": 1000,
                },
                # Flat after trend
                {
                    "high": 1.04,
                    "low": 1.02,
                    "open": 1.03,
                    "close": 1.03,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(
                        high=np.float64(1.15),
                        low=np.float64(1.13),
                        open=np.float64(1.14),
                        close=np.float64(1.14),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.14),
                        low=np.float64(1.12),
                        open=np.float64(1.13),
                        close=np.float64(1.13),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.13),
                        low=np.float64(1.11),
                        open=np.float64(1.12),
                        close=np.float64(1.12),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.15),
                        low=np.float64(1.13),
                        open=np.float64(1.14),
                        close=np.float64(1.14),
                        volume=np.float64(1000),
                    ),
                ],
                Trend=[
                    Candle(
                        high=np.float64(1.14),
                        low=np.float64(1.08),
                        open=np.float64(1.14),
                        close=np.float64(1.08),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.10),
                        low=np.float64(1.04),
                        open=np.float64(1.08),
                        close=np.float64(1.05),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.06),
                        low=np.float64(1.02),
                        open=np.float64(1.05),
                        close=np.float64(1.02),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.03),
                        low=np.float64(1.01),
                        open=np.float64(1.02),
                        close=np.float64(1.02),
                        volume=np.float64(1000),
                    ),
                ],
                Params=TradeParams(
                    direction=Direction.DOWN,
                    finish=True,
                    tp=0.0,
                    sl=0.0,
                ),
            )
        ],
    },
    {
        "name": "5. Downtrend with third candle stopping trend",
        "df": pd.DataFrame(
            [
                # Flat candles before downtrend
                {
                    "high": 1.15,
                    "low": 1.13,
                    "open": 1.14,
                    "close": 1.14,
                    "volume": 1000,
                },
                {
                    "high": 1.14,
                    "low": 1.12,
                    "open": 1.13,
                    "close": 1.13,
                    "volume": 1000,
                },
                {
                    "high": 1.13,
                    "low": 1.11,
                    "open": 1.12,
                    "close": 1.12,
                    "volume": 1000,
                },
                {
                    "high": 1.15,
                    "low": 1.13,
                    "open": 1.14,
                    "close": 1.14,
                    "volume": 1000,
                },
                # Start of downtrend (strictly decreasing highs and lows)
                {
                    "high": 1.14,
                    "low": 1.08,
                    "open": 1.14,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.10,
                    "low": 1.04,
                    "open": 1.08,
                    "close": 1.05,
                    "volume": 1000,
                },
                {
                    "high": 1.06,
                    "low": 1.02,
                    "open": 1.05,
                    "close": 1.02,
                    "volume": 1000,
                },
                # End of downtrend (highs and lows no longer decreasing)
                {
                    "high": 1.03,
                    "low": 1.01,
                    "open": 1.02,
                    "close": 1.02,
                    "volume": 1000,
                },
                {
                    "high": 1.03,
                    "low": 1.01,
                    "open": 1.02,
                    "close": 1.02,
                    "volume": 1000,
                },
                {
                    "high": 1.04,
                    "low": 1.02,
                    "open": 1.02,
                    "close": 1.03,
                    "volume": 1000,
                },
                # Flat after trend
                {
                    "high": 1.04,
                    "low": 1.02,
                    "open": 1.03,
                    "close": 1.03,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(
                        high=np.float64(1.15),
                        low=np.float64(1.13),
                        open=np.float64(1.14),
                        close=np.float64(1.14),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.14),
                        low=np.float64(1.12),
                        open=np.float64(1.13),
                        close=np.float64(1.13),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.13),
                        low=np.float64(1.11),
                        open=np.float64(1.12),
                        close=np.float64(1.12),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.15),
                        low=np.float64(1.13),
                        open=np.float64(1.14),
                        close=np.float64(1.14),
                        volume=np.float64(1000),
                    ),
                ],
                Trend=[
                    Candle(
                        high=np.float64(1.14),
                        low=np.float64(1.08),
                        open=np.float64(1.14),
                        close=np.float64(1.08),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.10),
                        low=np.float64(1.04),
                        open=np.float64(1.08),
                        close=np.float64(1.05),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.06),
                        low=np.float64(1.02),
                        open=np.float64(1.05),
                        close=np.float64(1.02),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.03),
                        low=np.float64(1.01),
                        open=np.float64(1.02),
                        close=np.float64(1.02),
                        volume=np.float64(1000),
                    ),
                    Candle(
                        high=np.float64(1.03),
                        low=np.float64(1.01),
                        open=np.float64(1.02),
                        close=np.float64(1.02),
                        volume=np.float64(1000),
                    ),
                ],
                Params=TradeParams(
                    direction=Direction.DOWN,
                    finish=True,
                    tp=0.0,
                    sl=0.0,
                ),
            )
        ],
    },
    {
        "name": "6. Uptrend followed by immediate downtrend with clear end",
        "df": pd.DataFrame(
            [
                # Flat candles before uptrend
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                {
                    "high": 1.01,
                    "low": 0.99,
                    "open": 1.00,
                    "close": 1.00,
                    "volume": 1000,
                },
                {
                    "high": 1.02,
                    "low": 1.00,
                    "open": 1.01,
                    "close": 1.01,
                    "volume": 1000,
                },
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                # Uptrend
                {
                    "high": 1.05,
                    "low": 1.02,
                    "open": 1.03,
                    "close": 1.04,
                    "volume": 1000,
                },
                {
                    "high": 1.08,
                    "low": 1.05,
                    "open": 1.06,
                    "close": 1.07,
                    "volume": 1000,
                },
                {
                    "high": 1.11,
                    "low": 1.08,
                    "open": 1.09,
                    "close": 1.10,
                    "volume": 1000,
                },
                # Peak candle (turnaround point)
                {
                    "high": 1.12,
                    "low": 1.08,
                    "open": 1.11,
                    "close": 1.10,
                    "volume": 1000,
                },
                # Downtrend
                {
                    "high": 1.10,
                    "low": 1.07,
                    "open": 1.08,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.07,
                    "low": 1.04,
                    "open": 1.05,
                    "close": 1.05,
                    "volume": 1000,
                },
                {
                    "high": 1.04,
                    "low": 1.01,
                    "open": 1.02,
                    "close": 1.02,
                    "volume": 1000,
                },
                # Breaks the downtrend (higher low and/or high)
                {
                    "high": 1.06,
                    "low": 1.03,
                    "open": 1.04,
                    "close": 1.05,
                    "volume": 1000,
                },
                {
                    "high": 1.08,
                    "low": 1.05,
                    "open": 1.06,
                    "close": 1.07,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(1.00, 0.98, 0.99, 0.99, 1000),
                    Candle(1.01, 0.99, 1.00, 1.00, 1000),
                    Candle(1.02, 1.00, 1.01, 1.01, 1000),
                    Candle(1.00, 0.98, 0.99, 0.99, 1000),
                ],
                Trend=[
                    Candle(1.05, 1.02, 1.03, 1.04, 1000),
                    Candle(1.08, 1.05, 1.06, 1.07, 1000),
                    Candle(1.11, 1.08, 1.09, 1.10, 1000),
                    Candle(1.12, 1.08, 1.11, 1.10, 1000),
                ],
                Params=TradeParams(direction=Direction.UP, finish=True, tp=0.0, sl=0.0),
            ),
            Segment(
                Pre=[
                    Candle(1.05, 1.02, 1.03, 1.04, 1000),
                    Candle(1.08, 1.05, 1.06, 1.07, 1000),
                    Candle(1.11, 1.08, 1.09, 1.10, 1000),
                    Candle(1.12, 1.08, 1.11, 1.10, 1000),
                ],
                Trend=[
                    Candle(1.10, 1.07, 1.08, 1.08, 1000),
                    Candle(1.07, 1.04, 1.05, 1.05, 1000),
                    Candle(1.04, 1.01, 1.02, 1.02, 1000),
                ],
                Params=TradeParams(
                    direction=Direction.DOWN, finish=True, tp=0.0, sl=0.0
                ),
            ),
        ],
    },
    {
        "name": "7. Two uptrends with bearish candle in between",
        "df": pd.DataFrame(
            [
                # Flat candles before first uptrend
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                {
                    "high": 1.01,
                    "low": 0.99,
                    "open": 1.00,
                    "close": 1.00,
                    "volume": 1000,
                },
                {
                    "high": 1.02,
                    "low": 1.00,
                    "open": 1.01,
                    "close": 1.01,
                    "volume": 1000,
                },
                {
                    "high": 1.00,
                    "low": 0.98,
                    "open": 0.99,
                    "close": 0.99,
                    "volume": 1000,
                },
                # First uptrend
                {
                    "high": 1.05,
                    "low": 1.02,
                    "open": 1.03,
                    "close": 1.04,
                    "volume": 1000,
                },
                {
                    "high": 1.08,
                    "low": 1.05,
                    "open": 1.06,
                    "close": 1.07,
                    "volume": 1000,
                },
                {
                    "high": 1.11,
                    "low": 1.08,
                    "open": 1.09,
                    "close": 1.10,
                    "volume": 1000,
                },
                # Bearish candle (stopping uptrend)
                {
                    "high": 1.09,
                    "low": 1.06,
                    "open": 1.08,
                    "close": 1.07,
                    "volume": 1000,
                },
                # Second uptrend
                {
                    "high": 1.12,
                    "low": 1.09,
                    "open": 1.10,
                    "close": 1.11,
                    "volume": 1000,
                },
                {
                    "high": 1.15,
                    "low": 1.12,
                    "open": 1.13,
                    "close": 1.14,
                    "volume": 1000,
                },
                {
                    "high": 1.18,
                    "low": 1.15,
                    "open": 1.16,
                    "close": 1.17,
                    "volume": 1000,
                },
                {
                    "high": 1.19,
                    "low": 1.15,
                    "open": 1.18,
                    "close": 1.16,
                    "volume": 1000,
                },
                # Bearish candle (stopping uptrend)
                {
                    "high": 1.18,
                    "low": 1.15,
                    "open": 1.16,
                    "close": 1.17,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(1.00, 0.98, 0.99, 0.99, 1000),
                    Candle(1.01, 0.99, 1.00, 1.00, 1000),
                    Candle(1.02, 1.00, 1.01, 1.01, 1000),
                    Candle(1.00, 0.98, 0.99, 0.99, 1000),
                ],
                Trend=[
                    Candle(1.05, 1.02, 1.03, 1.04, 1000),
                    Candle(1.08, 1.05, 1.06, 1.07, 1000),
                    Candle(1.11, 1.08, 1.09, 1.10, 1000),
                ],
                Params=TradeParams(direction=Direction.UP, finish=True, tp=0.0, sl=0.0),
            ),
            Segment(
                Pre=[
                    Candle(1.00, 0.98, 0.99, 0.99, 1000),
                    Candle(1.05, 1.02, 1.03, 1.04, 1000),
                    Candle(1.08, 1.05, 1.06, 1.07, 1000),
                    Candle(1.11, 1.08, 1.09, 1.10, 1000),
                ],
                Trend=[
                    Candle(1.09, 1.06, 1.08, 1.07, 1000),
                    Candle(1.12, 1.09, 1.10, 1.11, 1000),
                    Candle(1.15, 1.12, 1.13, 1.14, 1000),
                    Candle(1.18, 1.15, 1.16, 1.17, 1000),
                    Candle(1.19, 1.15, 1.18, 1.16, 1000),
                ],
                Params=TradeParams(direction=Direction.UP, finish=True, tp=0.0, sl=0.0),
            ),
        ],
    },
    {
        "name": "8. Downtrend followed by immediate uptrend with clear end",
        "df": pd.DataFrame(
            [
                # Flat candles before downtrend
                {
                    "high": 1.12,
                    "low": 1.10,
                    "open": 1.11,
                    "close": 1.11,
                    "volume": 1000,
                },
                {
                    "high": 1.13,
                    "low": 1.11,
                    "open": 1.12,
                    "close": 1.12,
                    "volume": 1000,
                },
                {
                    "high": 1.14,
                    "low": 1.12,
                    "open": 1.13,
                    "close": 1.13,
                    "volume": 1000,
                },
                {
                    "high": 1.13,
                    "low": 1.11,
                    "open": 1.12,
                    "close": 1.12,
                    "volume": 1000,
                },
                # Downtrend
                {
                    "high": 1.10,
                    "low": 1.07,
                    "open": 1.08,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.07,
                    "low": 1.04,
                    "open": 1.05,
                    "close": 1.05,
                    "volume": 1000,
                },
                {
                    "high": 1.04,
                    "low": 1.01,
                    "open": 1.02,
                    "close": 1.02,
                    "volume": 1000,
                },
                # Bottom candle (turnaround point)
                {
                    "high": 1.03,
                    "low": 1.00,
                    "open": 1.01,
                    "close": 1.02,
                    "volume": 1000,
                },
                # Uptrend
                {
                    "high": 1.06,
                    "low": 1.03,
                    "open": 1.04,
                    "close": 1.05,
                    "volume": 1000,
                },
                {
                    "high": 1.09,
                    "low": 1.06,
                    "open": 1.07,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.12,
                    "low": 1.09,
                    "open": 1.10,
                    "close": 1.11,
                    "volume": 1000,
                },
                # Breaks the uptrend
                {
                    "high": 1.10,
                    "low": 1.07,
                    "open": 1.09,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.11,
                    "low": 1.08,
                    "open": 1.09,
                    "close": 1.08,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(1.12, 1.10, 1.11, 1.11, 1000),
                    Candle(1.13, 1.11, 1.12, 1.12, 1000),
                    Candle(1.14, 1.12, 1.13, 1.13, 1000),
                    Candle(1.13, 1.11, 1.12, 1.12, 1000),
                ],
                Trend=[
                    Candle(1.10, 1.07, 1.08, 1.08, 1000),
                    Candle(1.07, 1.04, 1.05, 1.05, 1000),
                    Candle(1.04, 1.01, 1.02, 1.02, 1000),
                    Candle(1.03, 1.00, 1.01, 1.02, 1000),
                ],
                Params=TradeParams(
                    direction=Direction.DOWN, finish=True, tp=0.0, sl=0.0
                ),
            ),
            Segment(
                Pre=[
                    Candle(1.10, 1.07, 1.08, 1.08, 1000),
                    Candle(1.07, 1.04, 1.05, 1.05, 1000),
                    Candle(1.04, 1.01, 1.02, 1.02, 1000),
                    Candle(1.03, 1.00, 1.01, 1.02, 1000),
                ],
                Trend=[
                    Candle(1.06, 1.03, 1.04, 1.05, 1000),
                    Candle(1.09, 1.06, 1.07, 1.08, 1000),
                    Candle(1.12, 1.09, 1.10, 1.11, 1000),
                ],
                Params=TradeParams(direction=Direction.UP, finish=True, tp=0.0, sl=0.0),
            ),
        ],
    },
    {
        "name": "9. Two downtrends with bullish candle in between",
        "df": pd.DataFrame(
            [
                # Flat candles before first downtrend
                {
                    "high": 1.20,
                    "low": 1.18,
                    "open": 1.19,
                    "close": 1.19,
                    "volume": 1000,
                },
                {
                    "high": 1.21,
                    "low": 1.19,
                    "open": 1.20,
                    "close": 1.20,
                    "volume": 1000,
                },
                {
                    "high": 1.22,
                    "low": 1.20,
                    "open": 1.21,
                    "close": 1.21,
                    "volume": 1000,
                },
                {
                    "high": 1.21,
                    "low": 1.19,
                    "open": 1.20,
                    "close": 1.20,
                    "volume": 1000,
                },
                # First downtrend
                {
                    "high": 1.18,
                    "low": 1.15,
                    "open": 1.17,
                    "close": 1.16,
                    "volume": 1000,
                },
                {
                    "high": 1.15,
                    "low": 1.12,
                    "open": 1.14,
                    "close": 1.13,
                    "volume": 1000,
                },
                {
                    "high": 1.12,
                    "low": 1.09,
                    "open": 1.10,
                    "close": 1.10,
                    "volume": 1000,
                },
                # Bullish candle (stopping downtrend)
                {
                    "high": 1.14,
                    "low": 1.10,
                    "open": 1.11,
                    "close": 1.13,
                    "volume": 1000,
                },
                # Second downtrend
                {
                    "high": 1.13,
                    "low": 1.10,
                    "open": 1.12,
                    "close": 1.11,
                    "volume": 1000,
                },
                {
                    "high": 1.10,
                    "low": 1.07,
                    "open": 1.09,
                    "close": 1.08,
                    "volume": 1000,
                },
                {
                    "high": 1.08,
                    "low": 1.05,
                    "open": 1.07,
                    "close": 1.06,
                    "volume": 1000,
                },
                {
                    "high": 1.07,
                    "low": 1.04,
                    "open": 1.06,
                    "close": 1.05,
                    "volume": 1000,
                },
                # Bullish candle (stopping second downtrend)
                {
                    "high": 1.08,
                    "low": 1.05,
                    "open": 1.06,
                    "close": 1.07,
                    "volume": 1000,
                },
            ]
        ),
        "expected": [
            Segment(
                Pre=[
                    Candle(1.20, 1.18, 1.19, 1.19, 1000),
                    Candle(1.21, 1.19, 1.20, 1.20, 1000),
                    Candle(1.22, 1.20, 1.21, 1.21, 1000),
                    Candle(1.21, 1.19, 1.20, 1.20, 1000),
                ],
                Trend=[
                    Candle(1.18, 1.15, 1.17, 1.16, 1000),
                    Candle(1.15, 1.12, 1.14, 1.13, 1000),
                    Candle(1.12, 1.09, 1.10, 1.10, 1000),
                ],
                Params=TradeParams(
                    direction=Direction.DOWN, finish=True, tp=0.0, sl=0.0
                ),
            ),
            Segment(
                Pre=[
                    Candle(1.21, 1.19, 1.20, 1.20, 1000),
                    Candle(1.18, 1.15, 1.17, 1.16, 1000),
                    Candle(1.15, 1.12, 1.14, 1.13, 1000),
                    Candle(1.12, 1.09, 1.10, 1.10, 1000),
                ],
                Trend=[
                    Candle(1.14, 1.10, 1.11, 1.13, 1000),
                    Candle(1.13, 1.10, 1.12, 1.11, 1000),
                    Candle(1.10, 1.07, 1.09, 1.08, 1000),
                    Candle(1.08, 1.05, 1.07, 1.06, 1000),
                    Candle(1.07, 1.04, 1.06, 1.05, 1000),
                ],
                Params=TradeParams(
                    direction=Direction.DOWN, finish=True, tp=0.0, sl=0.0
                ),
            ),
        ],
    },
]


@pytest.mark.parametrize("case", test_cases, ids=[c["name"] for c in test_cases])
def test_marker_table_driven(case):
    marker = Marker(a_len=4)
    result = marker.mark(case["df"])
    assert len(result) == len(case["expected"]), f"Case: {case['name']}"
    for seg, expected_seg in zip(result, case["expected"]):
        assert seg.Pre == expected_seg.Pre
        assert seg.Trend == expected_seg.Trend
        assert seg.Params == expected_seg.Params
