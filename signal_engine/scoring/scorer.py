import pandas as pd
from .weighting import weights
from .risk_filters import volatility_filter

def score(momentum, trend, atr, price):
    raw = (
        momentum * weights["momentum"]
        + trend * weights["trend"]
        + (1 - (atr / price)) * weights["volatility"]
    )

    # apply risk filter
    adj = raw * volatility_filter(atr, price)
    return adj.clip(-1, 1)
