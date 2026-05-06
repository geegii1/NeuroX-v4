import json
import os

from alpaca.trading.client import TradingClient

ALPACA_KEY = "PKQRIXAXVIPNKXE7FJHPSXS3SE"
ALPACA_SECRET = "14fKSkkYhvw15FmGb2zrkAWc2qAsgGMAERmLrm9WpyCB"

client = TradingClient(ALPACA_KEY, ALPACA_SECRET, paper=True)

ORDERS_FILE = "data/open_orders.json"


class OrderManager:

    def __init__(self):
        self.orders = self._load()

    def _load(self):
        if not os.path.exists(ORDERS_FILE):
            return {}

        with open(ORDERS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}

    def _save(self):
        with open(ORDERS_FILE, "w") as f:
            json.dump(self.orders, f, indent=2)

    def exists(self, ticker):
        return ticker in self.orders

    def add(self, ticker, order_id, side, qty):
        self.orders[ticker] = {
            "order_id": order_id,
            "side": side,
            "qty": qty
        }
        self._save()

    def remove(self, ticker):
        if ticker in self.orders:
            del self.orders[ticker]
            self._save()

    def sync_with_broker(self):
        """
        Sync local orders with Alpaca.
        Remove anything that is no longer active.
        """

        updated_orders = {}

        for ticker, data in self.orders.items():
            order_id = data["order_id"]

            try:
                order = client.get_order_by_id(order_id)

                status = order.status

                if status in ["new", "partially_filled"]:
                    updated_orders[ticker] = data
                else:
                    print(f"[ORDER CLOSED] {ticker} → {status}")

            except Exception:
                # 🔥 KEY FIX: treat missing orders as closed
                print(f"[ORDER REMOVED] {ticker} → not found on broker")

        self.orders = updated_orders
        self._save()