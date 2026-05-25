import pandas as pd
import numpy as np
from src.data.fetch_data import fetch_stock_data

def calculate_signals(ticker):
    # Fetch data
    df = fetch_stock_data(ticker)

    # Moving average and standard deviation
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["std20"] = df["close"].rolling(window=20).std()

    # Bollinger Bands
    df["upper_band"] = df["ma20"] + (2 * df["std20"])
    df["lower_band"] = df["ma20"] - (2 * df["std20"])

    # Z-Score
    df["zscore"] = (df["close"] - df["ma20"]) / df["std20"]

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # Signal — all three conditions must be true
    df["signal"] = (
        (df["close"] < df["lower_band"]) &
        (df["zscore"] < -2) &
        (df["rsi"] < 30)
    ).astype(int)

    return df

if __name__ == "__main__":
    df = calculate_signals("AAPL")
    signals = df[df["signal"] == 1]
    print(f"Total signals found: {len(signals)}")
    print(signals[["close", "ma20", "zscore", "rsi"]].tail(10))