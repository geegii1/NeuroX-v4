import streamlit as st
import json
import os
import time
from dotenv import load_dotenv

# ===== CONFIG =====
st.set_page_config(page_title="WizeTrade", layout="wide")

DATA_PATH = "data"

# ===== STYLE =====
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.metric {
    font-size: 32px;
    font-weight: 700;
}

.subtle {
    color: #9ca3af;
    font-size: 13px;
}

.green { color: #22c55e; font-weight:600; }
.red { color: #ef4444; font-weight:600; }

.table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.table th {
    text-align: left;
    color: #9ca3af;
    font-size: 12px;
    padding-bottom: 8px;
}

.table td {
    padding: 12px 0;
    border-bottom: 1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)

# ===== ENV =====
load_dotenv("/home/ubuntu/NeuroX/.env")

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

client = StockHistoricalDataClient(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY")
)

# ===== HELPERS =====
def load_json(file):
    path = os.path.join(DATA_PATH, file)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def to_float(x):
    try:
        return float(x)
    except:
        return 0

def get_price(ticker):
    try:
        req = StockBarsRequest(
            symbol_or_symbols=[ticker],
            timeframe=TimeFrame.Minute,
            limit=1,
            feed="iex"
        )
        bars = client.get_stock_bars(req)

        if ticker in bars.data and bars.data[ticker]:
            return float(bars.data[ticker][-1].close)
    except:
        pass
    return None

# ===== LOAD =====
signal = load_json("latest_signal.json")
portfolio = load_json("open_orders.json")
last_run = load_json("last_run.json")

# ===== HEADER =====
st.markdown("# 🚀 WizeTrade")

last_run_ts = last_run.get("timestamp", "Never") if last_run else "Never"
st.caption(f"Last engine run: {last_run_ts}")

# ===== SIGNAL =====
st.markdown("### Today’s Signal")

if signal and "ticker" in signal:
    st.success(f"{signal.get('action')} {signal.get('ticker')}")
    st.caption(f"Confidence: {signal.get('confidence','N/A')}")
else:
    st.info("No signal")

# ===== CALCULATE =====
rows = []
total_value = 0
cost_basis = 0

for ticker, pos in portfolio.items():
    qty = to_float(pos.get("qty"))
    entry = to_float(pos.get("entry"))

    price = get_price(ticker)
    if price is None:
        price = entry

    value = qty * price
    cost = qty * entry
    pnl = value - cost

    total_value += value
    cost_basis += cost

    rows.append((ticker, qty, entry, price, pnl, pos.get("timestamp", "")))

total_pnl = total_value - cost_basis
pct = (total_pnl / cost_basis * 100) if cost_basis else 0

# ===== METRICS =====
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="subtle">Total Value</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">${total_value:,.2f}</div>', unsafe_allow_html=True)

with col2:
    color = "green" if total_pnl >= 0 else "red"
    st.markdown('<div class="subtle">PnL</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="{color} metric">${total_pnl:,.2f}</div>', unsafe_allow_html=True)

with col3:
    color = "green" if pct >= 0 else "red"
    st.markdown('<div class="subtle">Return</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="{color} metric">{pct:.2f}%</div>', unsafe_allow_html=True)

# ===== TABLE (FIXED RENDER) =====
st.markdown("### Portfolio")

table_html = """
<table class="table">
<tr>
<th>Ticker</th>
<th>Shares</th>
<th>Avg Cost</th>
<th>Current</th>
<th>PnL</th>
</tr>
"""

for ticker, qty, entry, price, pnl, timestamp in rows:
    color = "green" if pnl >= 0 else "red"
    ts_display = timestamp[:19] if timestamp else "—"

    table_html += f"""
    <tr>
        <td><b>{ticker}</b><br><span style="color:#6b7280;font-size:11px;font-family:'IBM Plex Mono',monospace">{ts_display}</span></td>
        <td>{qty}</td>
        <td>${entry:.2f}</td>
        <td>${price:.2f}</td>
        <td class="{color}">${pnl:.2f}</td>
    </tr>
    """

table_html += "</table>"

# 🚨 THIS LINE FIXES YOUR ISSUE
st.markdown(table_html, unsafe_allow_html=True)

# ===== AUTO REFRESH =====
time.sleep(60)
st.rerun()
