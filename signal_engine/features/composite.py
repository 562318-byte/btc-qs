import pandas as pd

def composite_momentum(rsi, macd_hist):
    # Weighted combo (these weights you can adjust anytime)
    return (0.6 * (rsi / 100)) + (0.4 * macd_hist)
