import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# ===== CONFIG =====
st.set_page_config(
    page_title="WizeTrade",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

DATA_PATH = "data"

# ===== THEME =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #07091e !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #e2e8f0 !important;
    overflow-x: hidden !important;
    max-width: 100vw !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 90% 55% at 50% -5%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 85% 85%, rgba(139,92,246,0.10) 0%, transparent 50%),
        linear-gradient(180deg, #07091e 0%, #0c1140 100%);
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    position: relative;
    z-index: 1;
    overflow-x: hidden !important;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="column"],
div[data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; }

/* ── NAV ── */
.wt-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: rgba(255,255,255,0.03);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: sticky; top: 0; z-index: 100;
    width: 100%;
}
.wt-brand { display: flex; align-items: center; gap: 9px; min-width: 0; }
.wt-mark {
    width: 30px; height: 30px; flex-shrink: 0;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 600; color: #fff;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35);
}
.wt-name { font-size: 15px; font-weight: 700; color: #fff; letter-spacing: -0.3px; white-space: nowrap; }
.wt-ver  { font-size: 10px; color: rgba(255,255,255,0.22); font-family: 'IBM Plex Mono', monospace; margin-left: 2px; white-space: nowrap; }
.wt-nav-r { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.wt-live {
    display: flex; align-items: center; gap: 5px;
    background: rgba(74,222,128,0.10);
    border: 1px solid rgba(74,222,128,0.2);
    padding: 4px 9px; border-radius: 20px;
    font-size: 10px; font-weight: 700; color: #4ade80;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.05em; white-space: nowrap;
}
.wt-live-dot { width: 6px; height: 6px; flex-shrink: 0; border-radius: 50%; background: #4ade80; animation: lp 2s infinite; }
@keyframes lp { 0%,100%{opacity:1} 50%{opacity:.4} }
.wt-offline {
    display: flex; align-items: center; gap: 5px;
    background: rgba(248,113,113,0.10);
    border: 1px solid rgba(248,113,113,0.2);
    padding: 4px 9px; border-radius: 20px;
    font-size: 10px; font-weight: 700; color: #f87171;
    font-family: 'IBM Plex Mono', monospace; white-space: nowrap;
}
.wt-time { font-size: 10px; color: rgba(255,255,255,0.18); font-family: 'IBM Plex Mono', monospace; white-space: nowrap; }

/* ── PAGE ── */
.wt-page { padding: 18px 14px 60px; width: 100%; overflow-x: hidden; }

/* ── SECTION LABEL ── */
.wt-slabel {
    font-size: 10px; font-weight: 600;
    color: rgba(255,255,255,0.28);
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-bottom: 10px;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── METRIC GRID: always 2×2 ── */
.wt-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
    margin-bottom: 18px;
    width: 100%;
}
.wt-mc {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 12px;
    min-width: 0;
    overflow: hidden;
}
.wt-mc-lbl {
    font-size: 10px; color: rgba(255,255,255,0.32);
    margin-bottom: 7px; letter-spacing: 0.01em;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.wt-mc-val {
    font-size: 18px; font-weight: 800;
    font-family: 'IBM Plex Mono', monospace;
    color: #fff; letter-spacing: -0.8px; line-height: 1;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.wt-mc-val.pos { color: #4ade80; }
.wt-mc-val.neg { color: #f87171; }
.wt-mc-sub { font-size: 9px; color: rgba(255,255,255,0.16); margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }

/* ── SIGNAL ── */
.wt-sig {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 18px;
    width: 100%;
    overflow: hidden;
}
.wt-sig-row1 {
    display: flex; align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
    gap: 8px;
    flex-wrap: wrap;
}
.wt-sig-left { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.wt-bdg {
    padding: 5px 11px; border-radius: 20px;
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
    white-space: nowrap;
}
.wt-bdg.BUY  { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.22); }
.wt-bdg.SELL { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.22); }
.wt-bdg.HOLD { background: rgba(251,191,36,0.12);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.22); }
.wt-bdg.NONE { background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.25); border: 1px solid rgba(255,255,255,0.07); }
.wt-sig-tkr  { font-size: 24px; font-weight: 800; color: #fff; letter-spacing: -1px; }
.wt-sig-strat { font-size: 10px; color: rgba(255,255,255,0.22); font-family: 'IBM Plex Mono', monospace; white-space: nowrap; }
.wt-conf-row {
    display: flex; justify-content: space-between;
    font-size: 10px; color: rgba(255,255,255,0.28);
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 6px;
}
.wt-conf-track { height: 4px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: hidden; }
.wt-conf-fill  { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #6366f1, #a78bfa); transition: width 0.4s ease; }
.wt-nosig { font-size: 12px; color: rgba(255,255,255,0.18); font-family: 'IBM Plex Mono', monospace; text-align: center; padding: 6px 0; }

/* ── TABLE ── */
.wt-tblcard {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 18px;
    width: 100%;
}
.wt-tbl-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; width: 100%; }
.wt-tbl { width: 100%; border-collapse: collapse; min-width: 280px; }
.wt-tbl thead tr { border-bottom: 1px solid rgba(255,255,255,0.06); }
.wt-tbl th {
    padding: 10px 14px;
    font-size: 10px; font-weight: 600;
    color: rgba(255,255,255,0.22);
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.07em; text-transform: uppercase;
    text-align: left; white-space: nowrap;
}
.wt-tbl td {
    padding: 13px 14px;
    font-size: 13px; font-family: 'IBM Plex Mono', monospace;
    color: rgba(255,255,255,0.5);
    border-bottom: 1px solid rgba(255,255,255,0.04);
    white-space: nowrap;
}
.wt-tbl tr:last-child td { border-bottom: none; }
.wt-tbl .tk { color: #fff; font-weight: 700; font-size: 14px; letter-spacing: 0.03em; }
.wt-tbl .cp { color: rgba(255,255,255,0.75); }
.wt-tbl .gn { color: #4ade80; font-weight: 600; }
.wt-tbl .rd { color: #f87171; font-weight: 600; }
.wt-sumrow {
    display: flex; align-items: center; justify-content: space-between;
    padding: 11px 14px;
    background: rgba(99,102,241,0.07);
    border-top: 1px solid rgba(99,102,241,0.12);
    flex-wrap: wrap; gap: 4px;
}
.wt-sumlbl { font-size: 11px; color: rgba(255,255,255,0.3); font-family: 'IBM Plex Mono', monospace; }
.wt-sumval { font-size: 13px; font-weight: 700; font-family: 'IBM Plex Mono', monospace; }
.wt-empty { padding: 40px 16px; text-align: center; color: rgba(255,255,255,0.12); font-size: 12px; font-family: 'IBM Plex Mono', monospace; }

/* ── FOOTER ── */
.wt-footer { text-align: center; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.04); }
.wt-fpill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    font-size: 10px; color: rgba(255,255,255,0.18);
    font-family: 'IBM Plex Mono', monospace;
}
.wt-fdot { width: 5px; height: 5px; border-radius: 50%; background: #6366f1; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }

/* ── EXTRA SMALL SCREENS (<360px) ── */
@media (max-width: 360px) {
    .wt-ver { display: none; }
    .wt-time { display: none; }
    .wt-mc-val { font-size: 16px; }
    .wt-sig-tkr { font-size: 20px; }
    .wt-tbl th, .wt-tbl td { padding: 10px 10px; font-size: 12px; }
}
</style>
""", unsafe_allow_html=True)


# ===== ENV & CLIENT =====
load_dotenv("/home/ubuntu/NeuroX/.env")
try:
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame
    client = StockHistoricalDataClient(
        os.getenv("ALPACA_API_KEY"),
        os.getenv("ALPACA_SECRET_KEY")
    )
    ALPACA_OK = True
except Exception:
    ALPACA_OK = False


# ===== HELPERS =====
def load_json(file):
    path = os.path.join(DATA_PATH, file)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def to_float(x):
    try: return float(x)
    except: return 0.0

def get_price(ticker):
    if not ALPACA_OK:
        return None
    try:
        req = StockBarsRequest(symbol_or_symbols=[ticker], timeframe=TimeFrame.Minute, limit=1, feed="iex")
        bars = client.get_stock_bars(req)
        if ticker in bars.data and bars.data[ticker]:
            return float(bars.data[ticker][-1].close)
    except Exception:
        pass
    return None


# ===== LOAD =====
signal    = load_json("latest_signal.json")
portfolio = load_json("open_orders.json")
now_str   = datetime.now().strftime("%H:%M")

# ===== COMPUTE =====
rows = []
total_value = 0.0
cost_basis  = 0.0

for ticker, pos in portfolio.items():
    qty   = to_float(pos.get("qty"))
    entry = to_float(pos.get("entry"))
    price = get_price(ticker) or entry
    value = qty * price
    cost  = qty * entry
    pnl   = value - cost
    pct   = (pnl / cost * 100) if cost else 0.0
    total_value += value
    cost_basis  += cost
    rows.append((ticker, qty, entry, price, pnl, pct))

total_pnl = total_value - cost_basis
total_pct = (total_pnl / cost_basis * 100) if cost_basis else 0.0
n_pos     = len(rows)

pnl_cls = "pos" if total_pnl >= 0 else "neg"
pct_cls = "pos" if total_pct >= 0 else "neg"
pnl_sign = "+" if total_pnl >= 0 else ""
pct_sign = "+" if total_pct >= 0 else ""
pnl_str  = f"{pnl_sign}${total_pnl:,.2f}"
pct_str  = f"{pct_sign}{total_pct:.2f}%"
sum_cls  = "gn" if total_pnl >= 0 else "rd"


# ─────────────────────────────────────────────────────────────
# NAV
# ─────────────────────────────────────────────────────────────
status_html = (
    '<div class="wt-live"><div class="wt-live-dot"></div>LIVE</div>'
    if ALPACA_OK else
    '<div class="wt-offline">OFFLINE</div>'
)

st.markdown(f"""
<div class="wt-nav">
  <div class="wt-brand">
    <div class="wt-mark">WT</div>
    <span class="wt-name">WizeTrade</span>
    <span class="wt-ver">v4</span>
  </div>
  <div class="wt-nav-r">
    {status_html}
    <span class="wt-time">{now_str} CT</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="wt-page">', unsafe_allow_html=True)


# ── METRICS ──────────────────────────────────────────────────
st.markdown('<div class="wt-slabel">Overview</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="wt-metrics">
  <div class="wt-mc">
    <div class="wt-mc-lbl">Total Value</div>
    <div class="wt-mc-val">${total_value:,.2f}</div>
    <div class="wt-mc-sub">portfolio NAV</div>
  </div>
  <div class="wt-mc">
    <div class="wt-mc-lbl">Unrealized P&L</div>
    <div class="wt-mc-val {pnl_cls}">{pnl_str}</div>
    <div class="wt-mc-sub">vs cost basis</div>
  </div>
  <div class="wt-mc">
    <div class="wt-mc-lbl">Return</div>
    <div class="wt-mc-val {pct_cls}">{pct_str}</div>
    <div class="wt-mc-sub">total</div>
  </div>
  <div class="wt-mc">
    <div class="wt-mc-lbl">Positions</div>
    <div class="wt-mc-val">{n_pos}</div>
    <div class="wt-mc-sub">open</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── SIGNAL ────────────────────────────────────────────────────
st.markdown('<div class="wt-slabel">Today\'s Signal</div>', unsafe_allow_html=True)

if signal and "ticker" in signal:
    action   = str(signal.get("action", "HOLD")).upper()
    sig_tkr  = signal.get("ticker", "—")
    strategy = signal.get("strategy", "—")
    conf_raw = signal.get("confidence", None)
    try:
        if conf_raw is None or str(conf_raw).strip() in ("", "N/A", "n/a", "—", "-"):
            conf = None
        else:
            conf = float(str(conf_raw).replace("%","").strip())
            conf = conf / 100 if conf > 1 else conf
    except Exception:
        conf = None
    cpct = min(max(conf * 100, 0), 100) if conf is not None else None
    conf_label = f"{cpct:.0f}%" if cpct is not None else "—"
    conf_fill  = f"{cpct:.1f}%" if cpct is not None else "0%"
    bcls = action if action in ("BUY","SELL","HOLD") else "NONE"

    st.markdown(f"""
<div class="wt-sig">
  <div class="wt-sig-row1">
    <div class="wt-sig-left">
      <span class="wt-bdg {bcls}">{action}</span>
      <span class="wt-sig-tkr">{sig_tkr}</span>
    </div>
    <span class="wt-sig-strat">{strategy}</span>
  </div>
  <div class="wt-conf-row"><span>Confidence</span><span>{conf_label}</span></div>
  <div class="wt-conf-track"><div class="wt-conf-fill" style="width:{conf_fill}"></div></div>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown('<div class="wt-sig"><div class="wt-nosig">No signal yet — engine warming up</div></div>', unsafe_allow_html=True)


# ── PORTFOLIO TABLE ───────────────────────────────────────────
st.markdown('<div class="wt-slabel">Portfolio</div>', unsafe_allow_html=True)
st.markdown('<div class="wt-tblcard">', unsafe_allow_html=True)

if rows:
    trows = ""
    for (t, qty, entry, price, pnl, pct) in rows:
        cls = "gn" if pnl >= 0 else "rd"
        arrow = "↑" if pnl >= 0 else "↓"
        sign  = "+" if pct >= 0 else ""
        trows += f"""<tr>
  <td class="tk">{t}</td>
  <td class="cp">${price:.2f}</td>
  <td class="{cls}">{arrow} {sign}{pct:.1f}%</td>
</tr>"""

    st.markdown(f"""
<div class="wt-tbl-scroll">
<table class="wt-tbl">
  <thead><tr><th>Ticker</th><th>Price</th><th>P&L</th></tr></thead>
  <tbody>{trows}</tbody>
</table>
</div>
<div class="wt-sumrow">
  <span class="wt-sumlbl">Total P&amp;L</span>
  <span class="wt-sumval {sum_cls}">{pnl_str} ({pct_str})</span>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown('<div class="wt-empty">No open positions</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────
st.markdown("""
<div class="wt-footer">
  <div class="wt-fpill">
    <div class="wt-fdot"></div>
    NeuroX v4 · auto-refresh 60s
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<script>setTimeout(()=>window.location.reload(),60000);</script>', unsafe_allow_html=True)
