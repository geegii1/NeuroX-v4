from datetime import datetime

# ===== CONFIG =====
STOP_LOSS_PCT = 0.05       # 5% loss
TAKE_PROFIT_PCT = 0.30     # 30% gain
TRAILING_STOP_PCT = 0.04   # 4% trail


def check_exit(ticker, position, current_price):
    entry = position.get("entry", 0)

    if entry <= 0:
        return None

    pnl_pct = (current_price - entry) / entry

    # ===== STOP LOSS =====
    if pnl_pct <= -STOP_LOSS_PCT:
        return {
            "action": "SELL",
            "reason": "STOP LOSS",
            "price": current_price
        }

    # ===== TAKE PROFIT =====
    if pnl_pct >= TAKE_PROFIT_PCT:
        return {
            "action": "SELL",
            "reason": "TAKE PROFIT",
            "price": current_price
        }

    # ===== TRAILING STOP =====
    peak = position.get("peak_price", entry)

    if current_price > peak:
        position["peak_price"] = current_price
        peak = current_price

    drawdown = (current_price - peak) / peak

    if drawdown <= -TRAILING_STOP_PCT:
        return {
            "action": "SELL",
            "reason": "TRAILING STOP",
            "price": current_price
        }

    return None


def execute_exit(ticker, position, current_price, trade_history):

    result = check_exit(ticker, position, current_price)

    if not result:
        return False

    entry = position.get("entry", 0)
    qty = position.get("qty", 0)

    pnl = (current_price - entry) * qty

    print(f"[EXIT] SELL {ticker} | Reason: {result['reason']}")
    print(f"PnL: ${round(pnl,2)} ({round((pnl/ (entry*qty))*100,2)}%)")

    trade_history.append({
        "ticker": ticker,
        "action": "SELL",
        "entry": entry,
        "exit": current_price,
        "qty": qty,
        "pnl": round(pnl, 2),
        "reason": result["reason"],
        "timestamp": str(datetime.now())
    })

    return True
