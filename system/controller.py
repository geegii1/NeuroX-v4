import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from system.signal_engine import rank_opportunities
from system.exit_engine import execute_exit

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

load_dotenv("/home/ubuntu/NeuroX/.env")

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)


def get_latest_price(ticker):
    try:
        request = StockBarsRequest(
            symbol_or_symbols=[ticker],
            timeframe=TimeFrame.Minute,
            start=datetime.utcnow() - timedelta(minutes=15),
            end=datetime.utcnow(),
            feed="iex"
        )

        bars = client.get_stock_bars(request)

        if ticker in bars.data:
            bar_list = bars.data[ticker]
            if len(bar_list) > 0:
                return float(bar_list[-1].close)

        print(f"[WARN] No bar data for {ticker}")
        return None

    except Exception as e:
        print(f"[PRICE ERROR] {ticker}: {e}")
        return None


class NeuroXController:

    def __init__(self):
        os.makedirs("data", exist_ok=True)

    def load_json(self, file, default):
        if os.path.exists(file):
            try:
                with open(file, "r") as f:
                    return json.load(f)
            except:
                return default
        return default

    def save_json(self, file, data):
        with open(file, "w") as f:
            json.dump(data, f, indent=2)

    def run(self):

        print("\n==============================")
        print("📊 WizeTrade Daily Brief")
        print("==============================\n")

        portfolio = self.load_json("data/open_orders.json", {})
        trade_history = self.load_json("data/trade_history.json", [])

        # ===== EXIT ENGINE =====
        for ticker in list(portfolio.keys()):
            price = get_latest_price(ticker)

            if price is None:
                continue

            exited = execute_exit(
                ticker,
                portfolio[ticker],
                price,
                trade_history
            )

            if exited:
                del portfolio[ticker]

        # ===== SIGNAL ENGINE =====
        opportunities = rank_opportunities()

        print("Top Opportunities:")
        for i, o in enumerate(opportunities[:3], 1):
            label = "STRONG" if o["score"] > 0.05 else "MODERATE"
            print(f"{i}. {o['ticker']} → {label} ({round(o['score']*100,2)}%)")

        if opportunities:
            top = opportunities[0]
            self.save_json("data/latest_signal.json", {
                "action": "BUY" if top["score"] > 0 else "HOLD",
                "ticker": top["ticker"],
                "score": round(top["score"] * 100, 2),
                "confidence": f"{round(top['score'] * 100, 2)}%",
                "timestamp": str(datetime.now())
            })

        selected = None
        for o in opportunities:
            if o["ticker"] not in portfolio:
                selected = o
                break

        if selected:
            ticker = selected["ticker"]

            print("\nDecision:")
            print(f"BUY {ticker}\n")

            price = get_latest_price(ticker)

            if price:
                portfolio[ticker] = {
                    "qty": 2,
                    "entry": round(price, 2),
                    "current_price": round(price, 2),
                    "peak_price": round(price, 2),
                    "timestamp": str(datetime.now())
                }

                print(f"[EXECUTED] BUY {ticker} @ {price}")
            else:
                print(f"[WARN] Skipping trade, no price for {ticker}")

        else:
            print("\nNo new trades\n")

        self.save_json("data/open_orders.json", portfolio)
        self.save_json("data/trade_history.json", trade_history)
        self.save_json("data/last_run.json", {"timestamp": str(datetime.now())})

        print("\nPortfolio:")
        print(f"Positions: {len(portfolio)}")
        print("\n==============================\n")
