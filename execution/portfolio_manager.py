import json
import os

POSITIONS_FILE = "data/positions.json"


class PortfolioManager:

    def __init__(self):
        self.positions = self._load()

    def _load(self):
        if not os.path.exists(POSITIONS_FILE):
            return {}

        with open(POSITIONS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}

    def _save(self):
        with open(POSITIONS_FILE, "w") as f:
            json.dump(self.positions, f, indent=2)

    def get_positions(self):
        return self.positions

    def add_position(self, ticker, qty, entry_price, atr):
        multiplier = 2

        stop_loss = entry_price - (atr * multiplier)

        self.positions[ticker] = {
            "qty": qty,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "atr": atr
        }

        print(f"[POSITION ADDED] {ticker} | Entry: {entry_price} | Stop: {stop_loss}")

        self._save()

    def update_trailing_stop(self, ticker, current_price):
        """
        🔥 TRAILING STOP LOGIC
        """

        if ticker not in self.positions:
            return

        pos = self.positions[ticker]

        atr = pos["atr"]
        multiplier = 2

        new_stop = current_price - (atr * multiplier)

        # 🔥 ONLY MOVE STOP UP (never down)
        if new_stop > pos["stop_loss"]:
            pos["stop_loss"] = new_stop

            print(f"[TRAILING STOP UPDATED] {ticker} → {new_stop}")

            self._save()

    def remove_position(self, ticker):
        if ticker in self.positions:
            del self.positions[ticker]
            self._save()