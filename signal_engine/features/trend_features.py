import pandas as pd
from . import composite

def trend_strength(ema_fast, ema_slow):
    spread = ema_fast - ema_slow
    return spread / ema_slow
