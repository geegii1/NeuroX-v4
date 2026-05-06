def apply_risk(signal, portfolio):

    if not signal:
        return None

    ticker = signal["ticker"]

    if ticker in portfolio:
        return None

    return {
        "ticker": ticker,
        "qty": 2,
        "price": 100,
        "stop_loss": 90
    }
