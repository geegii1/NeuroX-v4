import json
import os

TRADE_HISTORY_FILE = "data/trade_history.json"


def load_trades():
    if not os.path.exists(TRADE_HISTORY_FILE):
        return []
    with open(TRADE_HISTORY_FILE, "r") as f:
        return json.load(f)


def calculate_performance():
    trades = load_trades()

    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "pnl": 0,
            "max_drawdown": 0,
            "equity_curve": []
        }

    pnl_list = [t["pnl"] for t in trades]

    wins = [p for p in pnl_list if p > 0]
    win_rate = len(wins) / len(pnl_list) if pnl_list else 0

    equity = 0
    peak = 0
    max_dd = 0
    curve = []

    for p in pnl_list:
        equity += p
        peak = max(peak, equity)
        dd = peak - equity
        max_dd = max(max_dd, dd)
        curve.append(equity)

    return {
        "total_trades": len(pnl_list),
        "win_rate": round(win_rate * 100, 2),
        "pnl": round(sum(pnl_list), 2),
        "max_drawdown": round(max_dd, 2),
        "equity_curve": curve
    }


def print_equity_curve(curve):
    if not curve:
        print("No equity data yet")
        return

    print("\n📊 Equity Curve")
    max_val = max(curve) if curve else 1

    for v in curve[-20:]:  # last 20 points
        bar_len = int((v / max_val) * 30) if max_val > 0 else 0
        print("█" * bar_len)


def print_report():
    stats = calculate_performance()

    print("\n📈 Performance Summary")

    if stats["total_trades"] == 0:
        print("No completed trades yet")
        return

    print(f"Trades: {stats['total_trades']}")
    print(f"Win Rate: {stats['win_rate']}%")
    print(f"Total PnL: ${stats['pnl']}")
    print(f"Max Drawdown: ${stats['max_drawdown']}")

    print_equity_curve(stats["equity_curve"])
