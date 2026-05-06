from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pandas as pd

# ===== LOAD ENV =====
load_dotenv("/home/ubuntu/NeuroX/.env")

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise Exception("Missing Alpaca credentials")

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

# ===== CONFIG =====
TICKERS = ["TSLA", "AAPL", "ORCL", "NVDA", "AMD", "GOOG", "META", "AMZN"]

# ===== FETCH DATA (FIXED) =====
def get_market_data():
    end = datetime.utcnow()
    start = end - timedelta(days=60)

    request = StockBarsRequest(
        symbol_or_symbols=TICKERS,
        timeframe=TimeFrame.Day,
        start=start,
        end=end,
        feed="iex"
    )

    bars = client.get_stock_bars(request)

    data = {}

    for symbol in TICKERS:
        if symbol in bars.data:

            bar_list = bars.data[symbol]

            # 🔥 CONVERT LIST → DataFrame
            df = pd.DataFrame([{
                "timestamp": b.timestamp,
                "open": b.open,
                "high": b.high,
                "low": b.low,
                "close": b.close,
                "volume": b.volume
            } for b in bar_list])

            if not df.empty:
                df.set_index("timestamp", inplace=True)
                data[symbol] = df

    return data


# ===== SCORE ENGINE =====
def compute_score(df):
    try:
        close = df["close"]

        # need enough data
        if len(close) < 20:
            return 0

        momentum = (close.iloc[-1] / close.iloc[-20]) - 1
        volatility = close.pct_change().rolling(14).std().iloc[-1]

        return round(momentum - (volatility * 0.5), 4)

    except:
        return 0


# ===== RANK =====
def rank_opportunities():
    data = get_market_data()

    results = []

    for ticker, df in data.items():
        results.append({
            "ticker": ticker,
            "score": compute_score(df)
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
