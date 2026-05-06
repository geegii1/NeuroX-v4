import random


def generate_signal(macro, portfolio):

    tickers = ["INTC","AMD","QCOM","ORCL","GOOG","TSLA","AAPL"]

    candidates = []

    for t in tickers:
        momentum = random.uniform(-0.1, 0.8)

        confidence = "WEAK"
        if momentum > 0.6:
            confidence = "STRONG"
        elif momentum > 0.3:
            confidence = "MODERATE"

        candidates.append({
            "ticker": t,
            "momentum": momentum,
            "confidence": confidence
        })

    candidates = sorted(candidates, key=lambda x: x["momentum"], reverse=True)

    top = candidates[0]

    signal = {
        "action": "BUY",
        "ticker": top["ticker"],
        "confidence": top["confidence"],
        "reason": [
            f"Momentum strong ({round(top['momentum']*100,2)}%)",
            f"Market regime: {macro['mode']}"
        ],
        "stop_loss": round(100 * 0.9, 2),
        "risk_pct": "-10%"
    }

    return signal, candidates
