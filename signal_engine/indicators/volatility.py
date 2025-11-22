import pandas as pd

def atr(high, low, close, length: int = 14):
    tr = pd.concat([
        (high - low),
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    return tr.rolling(length).mean()
