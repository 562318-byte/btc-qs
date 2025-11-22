import ccxt
import pandas as pd
from datetime import datetime
from signal_engine.indicators import rsi, ema, macd, volatility, volume
from signal_engine.features import composite, trend_features
from signal_engine.scoring import scorer

# --- 1. Initialize exchange ---
exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1h'
limit = 1000  # last 1000 candles (~41 days)

# --- 2. Fetch OHLCV data ---
ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

# Optional: save CSV for later use
df.to_csv('btc_data.csv', index=False)

# --- 3. Compute indicators ---
df['RSI'] = rsi.rsi(df['Close'])
df['EMA'] = ema.ema(df['Close'])
macd_hist, macd_signal = macd.macd(df['Close'])
df['MACD_hist'] = macd_hist
df['ATR'] = volatility.atr(df['High'], df['Low'], df['Close'])
df['Volume_MA'] = volume.volume_ma(df['Volume'])

# --- 4. Feature engineering ---
df['Momentum_Score'] = composite.composite_momentum(df['RSI'], df['MACD_hist'])
df['Trend_Score'] = trend_features.trend_strength(df['EMA'], df['Close'])

# --- 5. Compute confidence score ---
df['Confidence'] = scorer.score(df['Momentum_Score'], df['Trend_Score'], df['ATR'], df['Close'])

# --- 6. Backtesting logic ---
initial_balance = 1000  # hypothetical USD
balance = initial_balance
position = 0  # BTC held
buy_threshold = 0.7
sell_threshold = -0.7

for i, row in df.iterrows():
    if row['Confidence'] > buy_threshold and position == 0:
        position = balance / row['Close']
        balance = 0
    elif row['Confidence'] < sell_threshold and position > 0:
        balance = position * row['Close']
        position = 0

# Final portfolio value
final_value = balance + (position * df.iloc[-1]['Close'] if position > 0 else 0)
print(f"Initial balance: ${initial_balance:.2f}")
print(f"Final portfolio value: ${final_value:.2f}")
print(f"Net return: {((final_value - initial_balance)/initial_balance)*100:.2f}%")

# --- 7. Print last few rows for reference ---
print(df.tail())
