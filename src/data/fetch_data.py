import yfinance as yf
import pandas as pd
from datetime import date

def fetch_stock_data(ticker, start="2020-01-01", end=None):
    if end is None:
        end = date.today().strftime("%Y-%m-%d")
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    df = df[["Close", "Volume"]]
    df.columns = ["close", "volume"]
    df.index.name = "date"
    return df

if __name__ == "__main__":
    df = fetch_stock_data("AAPL")
    print(df.head())
    print(f"Total rows: {len(df)}")