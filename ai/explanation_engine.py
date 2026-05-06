def generate_explanation(signal, regime, macro):
    """
    Generates human-readable explanation for a trade decision
    """

    # --- SAFE ACCESS ---
    ticker = signal.get("ticker", "UNKNOWN")
    momentum = signal.get("momentum", 0)
    price = signal.get("price", 0)
    atr = signal.get("atr", 0)

    # --- CALCULATIONS ---
    momentum_pct = round(momentum * 100, 2)
    stop_loss = round(price - (atr * 2), 2) if price and atr else 0
    risk_pct = round(((atr * 2) / price) * 100, 2) if price else 0

    confidence = get_confidence(momentum)

    # --- BUILD EXPLANATION ---
    explanation = f"""
=== WizeTrade Signal ===

Action: BUY {ticker}
Confidence: {confidence}

Reason:
- Momentum (20d): {momentum_pct}%
- Market regime: {regime}
- Macro environment: {macro}
- Volatility (ATR): {round(atr, 2)}
- Price: ${round(price, 2)}

Risk:
- Stop Loss: ${stop_loss}
- Estimated Risk: -{risk_pct}%
"""

    return explanation.strip()


def get_confidence(momentum):
    """
    Converts momentum score into human-readable confidence
    """
    if momentum > 0.5:
        return "STRONG"
    elif momentum > 0.2:
        return "MODERATE"
    else:
        return "WEAK"
