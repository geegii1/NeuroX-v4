import json
import os

DATA_FILE = "data/open_orders.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def clean_portfolio():

    portfolio = load_json(DATA_FILE, {})

    if not portfolio:
        print("[INFO] No portfolio data found.")
        return

    cleaned = {}
    removed = []

    for ticker, pos in portfolio.items():

        entry = pos.get("entry", 0)
        qty = pos.get("qty", 0)

        # ❌ Remove bad data
        if entry == 0 or qty == 0:
            removed.append(ticker)
            continue

        cleaned[ticker] = pos

    # Save cleaned version
    save_json(DATA_FILE, cleaned)

    print("\n===== DATA CLEANUP COMPLETE =====")

    if removed:
        print("Removed corrupted positions:")
        for t in removed:
            print(f" - {t}")
    else:
        print("No corrupted positions found.")

    print(f"\nRemaining positions: {len(cleaned)}")
    print("================================\n")


if __name__ == "__main__":
    clean_portfolio()
